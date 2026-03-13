"""
Interactive GUI for Pfirrmann grade validation.

A Tkinter desktop application enabling radiologists to:
    1. View side-by-side T1 and T2 mid-sagittal MRI images (700x700 canvas)
    2. Inspect IVD height measurement overlays (colour-coded by disc level)
    3. Review the original Pfirrmann grade for D5, D4, D3
    4. Override grades using dropdown selectors (1--5)
    5. Mark individual disc grades as validated
    6. Navigate between 515 patients
    7. Export an updated CSV with original/overridden/validated columns

Colour Convention:
    Red   = D5 (L5-S1)
    Green = D4 (L4-L5)
    Cyan  = D3 (L3-L4)

Required data paths (configurable in __init__):
    - Sagittal images directory (T1_XXXX_*.png, T2_XXXX_*.png)
    - PfirrmannGrade.csv
    - IVDHeights_Corrected.csv

Usage:
    python pfirrmann_validator.py
"""

import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageTk


class PfirrmannValidator:
    def __init__(self, root):
        self.root = root
        self.root.title("Pfirrmann Grade Validator - LSMA-PQR")
        self.root.geometry("1600x900")

        # ---- Data paths (update these for your local setup) ----
        self.base_dir = Path(r"d:\2.2 Dataset_s\RFM_Dataset")
        self.images_dir = self.base_dir / "Sagittal" / "images"
        self.pfirrmann_csv = self.base_dir / "PfirrmannGrade" / "PfirrmannGrade.csv"
        self.ivd_heights_csv = self.base_dir / "IVDHt" / "IVDHeights_Corrected.csv"
        self.edits_file = self.base_dir / "PfirrmannGrade" / "pfirrmann_edits.json"

        self.df_pfirrmann = pd.read_csv(self.pfirrmann_csv)
        self.df_ivd = pd.read_csv(self.ivd_heights_csv)
        self.edits = self._load_edits()
        self.patient_ids = sorted(int(p) for p in self.df_pfirrmann["Patient_ID"].unique())
        self.current_patient_idx = 0

        self._build_ui()
        self._load_patient(self.patient_ids[0])

    # ------------------------------------------------------------------ IO
    def _load_edits(self):
        if self.edits_file.exists():
            with open(self.edits_file) as f:
                return json.load(f)
        return {}

    def _save_edits(self):
        with open(self.edits_file, "w") as f:
            json.dump(self.edits, f, indent=2)

    # -------------------------------------------------------------- UI
    def _build_ui(self):
        main = ttk.Frame(self.root, padding="10")
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        # Header
        hdr = ttk.Frame(main)
        hdr.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 10))
        ttk.Label(hdr, text="Patient ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        self.lbl_pid = ttk.Label(hdr, text="", font=("Arial", 12))
        self.lbl_pid.grid(row=0, column=1, padx=5)
        self.lbl_count = ttk.Label(hdr, text="", font=("Arial", 10))
        self.lbl_count.grid(row=0, column=3, padx=5)
        self.lbl_edit = ttk.Label(hdr, text="", font=("Arial", 10), foreground="blue")
        self.lbl_edit.grid(row=0, column=4, padx=20)

        nav = ttk.Frame(hdr)
        nav.grid(row=0, column=5, padx=20)
        ttk.Button(nav, text="Previous", command=self._prev).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav, text="Next", command=self._next).pack(side=tk.LEFT, padx=5)
        ttk.Button(hdr, text="Save Edits", command=self._save_current).grid(row=0, column=6, padx=10)
        ttk.Button(hdr, text="Export CSV", command=self._export_csv).grid(row=0, column=7, padx=5)

        # Image canvases
        imgs = ttk.Frame(main)
        imgs.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        imgs.columnconfigure(0, weight=1)
        imgs.columnconfigure(1, weight=1)

        t1f = ttk.LabelFrame(imgs, text="T1 Modality", padding="10")
        t1f.grid(row=0, column=0, sticky="nsew", padx=5)
        self.cvs_t1 = tk.Canvas(t1f, width=700, height=700, bg="black")
        self.cvs_t1.pack()

        t2f = ttk.LabelFrame(imgs, text="T2 Modality", padding="10")
        t2f.grid(row=0, column=1, sticky="nsew", padx=5)
        self.cvs_t2 = tk.Canvas(t2f, width=700, height=700, bg="black")
        self.cvs_t2.pack()

        # Controls
        ctrl = ttk.LabelFrame(main, text="Pfirrmann Grade Validation", padding="15")
        ctrl.grid(row=2, column=0, columnspan=2, sticky="we", pady=10)

        self.grade_vars, self.check_vars = {}, {}
        for i, (lbl, key) in enumerate([
            ("D5 (L5-S1)", "D5"), ("D4 (L4-L5)", "D4"), ("D3 (L3-L4)", "D3")
        ]):
            f = ttk.Frame(ctrl)
            f.grid(row=0, column=i, padx=20, pady=5)
            ttk.Label(f, text=lbl, font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

            ttk.Label(f, text="Original:").grid(row=1, column=0, sticky="w")
            ol = ttk.Label(f, text="", font=("Arial", 10, "bold"), foreground="blue")
            ol.grid(row=1, column=1, columnspan=2, sticky="w")
            setattr(self, f"lbl_{key}_orig", ol)

            ttk.Label(f, text="Override:").grid(row=2, column=0, sticky="w", pady=5)
            gv = tk.StringVar(value="")
            ttk.Combobox(f, textvariable=gv, values=["", "1", "2", "3", "4", "5"],
                         width=8, state="readonly").grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
            self.grade_vars[key] = gv

            cv = tk.BooleanVar(value=False)
            ttk.Checkbutton(f, text="Validated", variable=cv).grid(row=3, column=0, columnspan=3, pady=5)
            self.check_vars[key] = cv

            ttk.Label(f, text="IVD Height:").grid(row=4, column=0, sticky="w")
            hl = ttk.Label(f, text="")
            hl.grid(row=4, column=1, columnspan=2, sticky="w")
            setattr(self, f"lbl_{key}_ht", hl)

        # Reference
        ref = ttk.LabelFrame(main, text="Pfirrmann Grading Reference", padding="10")
        ref.grid(row=3, column=0, columnspan=2, sticky="we", pady=10)
        ttk.Label(ref, justify=tk.LEFT, font=("Arial", 9), text=(
            "Grade 1: Bright hyperintense nucleus, homogeneous, clear height\n"
            "Grade 2: Hyperintense nucleus, horizontal band, clear height\n"
            "Grade 3: Intermediate gray, inhomogeneous, slightly decreased height\n"
            "Grade 4: Hypointense dark gray, lost distinction, moderate height loss\n"
            "Grade 5: Hypointense black, inhomogeneous, collapsed disc space"
        )).pack()

    # --------------------------------------------------------- Patient loading
    def _load_patient(self, pid):
        self.current_pid = pid
        ps = str(pid).zfill(4)
        self.lbl_pid.config(text=ps)
        idx = self.patient_ids.index(pid)
        self.lbl_count.config(text=f"{idx + 1} / {len(self.patient_ids)}")

        self.t1_path = next(self.images_dir.glob(f"T1_{ps}_*.png"), None)
        self.t2_path = next(self.images_dir.glob(f"T2_{ps}_*.png"), None)

        row = self.df_pfirrmann[self.df_pfirrmann["Patient_ID"] == pid]
        self.orig_grades = {k: int(row.iloc[0][k]) for k in ["D5", "D4", "D3"]} if not row.empty else {"D5": 0, "D4": 0, "D3": 0}

        ivd_row = self.df_ivd[self.df_ivd["Patient_ID"] == pid]
        if not ivd_row.empty:
            self.ivd_ht = {k: float(ivd_row.iloc[0][f"{k}_Ht"]) for k in ["D5", "D4", "D3"]}
            self.ivd_coord = {k: ivd_row.iloc[0][f"{k}_Coord"] for k in ["D5", "D4", "D3"]}
        else:
            self.ivd_ht = {"D5": 0, "D4": 0, "D3": 0}
            self.ivd_coord = {"D5": "", "D4": "", "D3": ""}

        for k in ["D5", "D4", "D3"]:
            getattr(self, f"lbl_{k}_orig").config(text=str(self.orig_grades[k]))
            getattr(self, f"lbl_{k}_ht").config(text=f"{self.ivd_ht[k]:.2f} mm")

        pk = str(pid)
        if pk in self.edits:
            ed = self.edits[pk]
            for k in ["D5", "D4", "D3"]:
                v = ed.get(f"{k}_override")
                self.grade_vars[k].set(str(v) if v else "")
                self.check_vars[k].set(ed.get(f"{k}_validated", False))
            self.lbl_edit.config(text="Has Edits", foreground="orange")
        else:
            for k in ["D5", "D4", "D3"]:
                self.grade_vars[k].set("")
                self.check_vars[k].set(False)
            self.lbl_edit.config(text="")

        self._show_images()

    def _show_images(self):
        for path, canvas, mod in [(self.t1_path, self.cvs_t1, "T1"),
                                   (self.t2_path, self.cvs_t2, "T2")]:
            if path and path.exists():
                img = Image.open(path).convert("RGB")
                img = self._annotate(img, mod)
                img = img.resize((700, 700), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                setattr(self, f"_photo_{mod}", photo)
                canvas.create_image(350, 350, image=photo)
            else:
                canvas.delete("all")
                canvas.create_text(350, 350, text=f"{mod} Not Found", fill="white", font=("Arial", 14))

    def _annotate(self, img, modality):
        draw = ImageDraw.Draw(img)
        try:
            fl, fs = ImageFont.truetype("arial.ttf", 20), ImageFont.truetype("arial.ttf", 14)
        except OSError:
            fl = fs = ImageFont.load_default()

        colours = {"D5": "#FF0000", "D4": "#00FF00", "D3": "#00FFFF"}
        labels = {"D5": "L5-S1", "D4": "L4-L5", "D3": "L3-L4"}

        for k in ["D5", "D4", "D3"]:
            cs = self.ivd_coord[k]
            if not cs or ";" not in str(cs):
                continue
            try:
                ts, bs = str(cs).split(";")
                tx, ty = map(float, ts.split(","))
                bx, by = map(float, bs.split(","))
                c = colours[k]
                draw.line([(tx, ty), (bx, by)], fill=c, width=3)
                draw.ellipse([(tx - 4, ty - 4), (tx + 4, ty + 4)], fill=c, outline="white", width=2)
                draw.ellipse([(bx - 4, by - 4), (bx + 4, by + 4)], fill=c, outline="white", width=2)
                mx, my = (tx + bx) / 2 + 15, (ty + by) / 2 - 30
                for j, txt in enumerate([labels[k], f"H:{self.ivd_ht[k]:.1f}mm", f"PG:{self.orig_grades[k]}"]):
                    pos = (mx, my + j * 18)
                    bb = draw.textbbox(pos, txt, font=fs)
                    draw.rectangle([(bb[0] - 2, bb[1] - 2), (bb[2] + 2, bb[3] + 2)], fill="black", outline=c)
                    draw.text(pos, txt, fill=c, font=fs)
            except (ValueError, TypeError):
                pass

        ptxt = f"Patient {str(self.current_pid).zfill(4)} - {modality}"
        bb = draw.textbbox((10, 10), ptxt, font=fl)
        draw.rectangle([(bb[0] - 5, bb[1] - 5), (bb[2] + 5, bb[3] + 5)], fill="black", outline="white", width=2)
        draw.text((10, 10), ptxt, fill="white", font=fl)
        return img

    # ----------------------------------------------------------- Actions
    def _save_current(self):
        pk = str(self.current_pid)
        ed, changed = {}, False
        for k in ["D5", "D4", "D3"]:
            v = self.grade_vars[k].get()
            ed[f"{k}_override"] = int(v) if v else None
            ed[f"{k}_validated"] = self.check_vars[k].get()
            if v or ed[f"{k}_validated"]:
                changed = True
        if changed:
            self.edits[pk] = ed
            self.lbl_edit.config(text="Has Edits", foreground="orange")
        elif pk in self.edits:
            del self.edits[pk]
            self.lbl_edit.config(text="")
        self._save_edits()
        messagebox.showinfo("Saved", f"Edits saved for Patient {pk}")

    def _export_csv(self):
        df = self.df_pfirrmann.copy()
        for c in ["D5", "D4", "D3"]:
            df[f"{c}_Original"] = df[c]
            df[f"{c}_Validated"] = False
            df[f"{c}_Edited"] = False

        for pid_str, ed in self.edits.items():
            mask = df["Patient_ID"] == int(pid_str)
            for k in ["D5", "D4", "D3"]:
                o = ed.get(f"{k}_override")
                if o is not None:
                    df.loc[mask, k] = o
                    df.loc[mask, f"{k}_Edited"] = True
                if ed.get(f"{k}_validated"):
                    df.loc[mask, f"{k}_Validated"] = True

        out = self.base_dir / "PfirrmannGrade" / "PfirrmannGrade_Updated.csv"
        df.to_csv(out, index=False)

        summary = self.base_dir / "PfirrmannGrade" / "validation_summary.txt"
        with open(summary, "w") as f:
            f.write("Pfirrmann Grade Validation Summary\n" + "=" * 60 + "\n\n")
            f.write(f"Total Patients: {len(df)}\nPatients with Edits: {len(self.edits)}\n\n")
            for d in ["D5", "D4", "D3"]:
                f.write(f"{d}: Edited={df[f'{d}_Edited'].sum()}, Validated={df[f'{d}_Validated'].sum()}\n")

        messagebox.showinfo("Exported", f"CSV: {out}\nSummary: {summary}\nEdited patients: {len(self.edits)}")

    def _prev(self):
        if self.current_patient_idx > 0:
            self.current_patient_idx -= 1
            self._load_patient(self.patient_ids[self.current_patient_idx])

    def _next(self):
        if self.current_patient_idx < len(self.patient_ids) - 1:
            self.current_patient_idx += 1
            self._load_patient(self.patient_ids[self.current_patient_idx])


if __name__ == "__main__":
    root = tk.Tk()
    PfirrmannValidator(root)
    root.mainloop()
