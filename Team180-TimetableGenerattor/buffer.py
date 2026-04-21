import csv
import random
import customtkinter as ctk
from tkinter import ttk, messagebox

#THEME
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


#SMART GENERATOR
def generate(classes, subjects, teachers, hours, days, slots):
    timetable = {c: [["Free"] * slots for _ in days] for c in classes}
    subject_count = {c: {sub: 0 for sub in subjects} for c in classes}
    teacher_busy = {t: [[False]*slots for _ in days] for t in teachers}

    for c in classes:
        for i, sub in enumerate(subjects):
            teacher = teachers[i % len(teachers)]
            required = hours[i]

            attempts = 0
            while subject_count[c][sub] < required and attempts < 500:
                d = random.randint(0, len(days)-1)
                s = random.randint(0, slots-1)

                if timetable[c][d][s] != "Free":
                    attempts += 1
                    continue

                if teacher_busy[teacher][d][s]:
                    attempts += 1
                    continue

                # no consecutive same subject
                if s > 0 and sub in timetable[c][d][s-1]:
                    attempts += 1
                    continue

                # max 2 per day
                if sum(1 for x in timetable[c][d] if sub in x) >= 2:
                    attempts += 1
                    continue

                timetable[c][d][s] = f"{sub} ({teacher})"
                teacher_busy[teacher][d][s] = True
                subject_count[c][sub] += 1

            # fallback
            if subject_count[c][sub] < required:
                for d in range(len(days)):
                    for s in range(slots):
                        if timetable[c][d][s] == "Free":
                            timetable[c][d][s] = f"{sub} ({teacher})"
                            teacher_busy[teacher][d][s] = True
                            subject_count[c][sub] += 1
                            if subject_count[c][sub] >= required:
                                break
                    if subject_count[c][sub] >= required:
                        break

    return timetable


#CSV
def save_csv(timetable, classes, days, slots):
    for c in classes:
        with open(f"{c}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            times = [f"{9+i}:00-{10+i}:00" for i in range(slots)]
            writer.writerow(["Day"] + times)

            for d in range(len(days)):
                writer.writerow([days[d]] + timetable[c][d])

    messagebox.showinfo("Saved", "CSV files saved successfully!")


#UI
def show_ui():
    app = ctk.CTk()
    app.geometry("1400x800")
    app.title("Smart Timetable Generator")

    timetable_data = {}

    # COLORS (SOFT AESTHETIC)
    BG = "#F5F7FB"
    PANEL = "#E9EEF6"
    CARD = "#FFFFFF"
    ACCENT = "#4F8EF7"
    TEXT = "#1F2937"
    FREE = "#FECACA"

    app.configure(fg_color=BG)

    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # SIDEBAR
    sidebar = ctk.CTkFrame(app, width=300, fg_color=PANEL, corner_radius=15)
    sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
    sidebar.grid_propagate(False)

    ctk.CTkLabel(sidebar, text="Input Panel",
                 text_color=TEXT,
                 font=("Segoe UI", 20, "bold")).pack(pady=20)

    def create_entry(label):
        ctk.CTkLabel(sidebar, text=label, text_color=TEXT).pack(anchor="w", padx=20)
        e = ctk.CTkEntry(sidebar, width=240)
        e.pack(padx=20, pady=6)
        return e

    class_entry = create_entry("Classes (A,B,C)")
    subject_entry = create_entry("Subjects")
    teacher_entry = create_entry("Teachers")
    hours_entry = create_entry("Hours")
    days_entry = create_entry("Days")
    slots_entry = create_entry("Slots")

    #MAIN AREA
    main_area = ctk.CTkFrame(app, fg_color=BG)
    main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    main_area.grid_rowconfigure(0, weight=1)
    main_area.grid_columnconfigure(0, weight=1)

    notebook = ttk.Notebook(main_area)
    notebook.grid(row=0, column=0, sticky="nsew")

    #GENERATE
    def generate_ui():
        nonlocal timetable_data

        for tab in notebook.tabs():
            notebook.forget(tab)

        try:
            classes = [x.strip() for x in class_entry.get().split(",") if x.strip()]
            subjects = [x.strip() for x in subject_entry.get().split(",") if x.strip()]
            teachers = [x.strip() for x in teacher_entry.get().split(",") if x.strip()]
            days = [x.strip() for x in days_entry.get().split(",") if x.strip()]
            hours = [int(x.strip()) for x in hours_entry.get().split(",")]
            slots = int(slots_entry.get())

            if len(subjects) != len(hours):
                messagebox.showerror("Error", "Subjects and hours must match!")
                return

            if sum(hours) > len(days) * slots:
                messagebox.showerror("Error", "Too many hours!")
                return

        except:
            messagebox.showerror("Error", "Invalid input")
            return

        timetable_data = generate(classes, subjects, teachers, hours, days, slots)

        for c in classes:
            frame = ctk.CTkFrame(notebook, fg_color=BG)
            notebook.add(frame, text=c)

            scroll = ctk.CTkScrollableFrame(frame, fg_color=BG)
            scroll.pack(fill="both", expand=True, padx=10, pady=10)

            times = [f"{9+i}:00-{10+i}:00" for i in range(slots)]

            # HEADER
            for s in range(slots):
                ctk.CTkLabel(scroll, text=times[s],
                             fg_color=ACCENT, text_color="white",
                             corner_radius=8, width=130).grid(row=0, column=s+1, padx=6, pady=6)

            for d in range(len(days)):
                ctk.CTkLabel(scroll, text=days[d],
                             fg_color="#CBD5F5", text_color=TEXT,
                             corner_radius=8, width=100).grid(row=d+1, column=0, padx=6, pady=6)

                for s in range(slots):
                    val = timetable_data[c][d][s]
                    color = CARD if val != "Free" else FREE

                    ctk.CTkLabel(scroll,
                                 text=val.replace(" (", "\n("),
                                 width=130,
                                 height=80,
                                 corner_radius=12,
                                 fg_color=color,
                                 text_color=TEXT).grid(row=d+1, column=s+1, padx=6, pady=6)

        save_btn.configure(command=lambda: save_csv(timetable_data, classes, days, slots))

    #BUTTONS
    ctk.CTkButton(sidebar, text="Generate",
                  command=generate_ui,
                  fg_color=ACCENT,
                  height=40).pack(pady=15)

    save_btn = ctk.CTkButton(sidebar, text="Save CSV",
                             fg_color="#34D399",
                             height=40)
    save_btn.pack(pady=5)

    app.mainloop()


#MAIN
if __name__ == "__main__":
    show_ui()
