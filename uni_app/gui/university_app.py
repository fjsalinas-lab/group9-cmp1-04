import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from uni_app.model.database import Database
from uni_app.model.student import Student, EMAIL_RE, PASS_RE
from uni_app.model.subject import Subject

class UniversityApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.current_student = None
        
        self.setup_ui()
        
    def setup_ui(self):

        self.root.title("University System")
        self.root.geometry("650x550")
        self.root.minsize(600, 500)
        self.root.configure(bg="white")
        
        
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=10)
        self.root.option_add("*Font", default_font)
        
        self.container = ttk.Frame(self.root, style="Main.TFrame")
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frames = {}

        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()

        
        self.frames["login"] = self.login_frame
        self.frames["register"] = self.register_frame
        
        self.show_frame("login")
    
    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)
    
    def create_login_frame(self):

        login_frame = ttk.Frame(self.container, style="Main.TFrame", padding=(10, 5))
        
        ttk.Label(
            login_frame, 
            text="Login",
            style="Header.TLabel"
        ).pack(pady=(20, 30))
       

        form_frame = ttk.Frame(login_frame)
        form_frame.pack(padx=50)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, show="•")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        form_frame.columnconfigure(1, weight=1)
        
        button_frame = ttk.Frame(login_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.login, 
                   width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Register", 
                   command=lambda: self.show_frame("register"), 
                   width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit, 
                   width=12).pack(side=tk.LEFT, padx=5)
       
        return login_frame
    
    def create_register_frame(self):

        register_frame = ttk.Frame(self.container, style="Main.TFrame", padding=(10, 5))
        
        ttk.Label(
            register_frame, 
            text="Registration",
            style="Header.TLabel"
        ).pack(pady=(20, 30))
        
        form_frame = ttk.Frame(register_frame)
        form_frame.pack(padx=50)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_name_entry = ttk.Entry(form_frame, width=30)
        self.reg_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_email_entry = ttk.Entry(form_frame, width=30)
        self.reg_email_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_password_entry = ttk.Entry(form_frame, width=30, show="•")
        self.reg_password_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Confirm Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_confirm_password_entry = ttk.Entry(form_frame, width=30, show="•")
        self.reg_confirm_password_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        form_frame.columnconfigure(1, weight=1)
        
        button_frame = ttk.Frame(register_frame)
        button_frame.pack(pady=20)
        
        register_button = ttk.Button(button_frame, text="Register", command=self.register, 
                   width=15)
        register_button.pack(side=tk.LEFT, padx=5)
        
        login_button = ttk.Button(button_frame, text="Back to Login", 
                   command=lambda: self.show_frame("login"), 
                   width=15)
        login_button.pack(side=tk.LEFT, padx=5)
        
        return register_frame
    
    def create_dashboard_frame(self, student):
 
        dashboard_frame = ttk.Frame(self.container, style="Main.TFrame", padding=(10, 5))
        
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            header_frame, 
            text="University System",
            style="Header.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            header_frame,
            text=f"{student.name} ({student.id})"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            header_frame,
            text="Logout",
            command=self.logout,
            width=10
        ).pack(side=tk.RIGHT)
        
        notebook = ttk.Notebook(dashboard_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        subjects_tab = ttk.Frame(notebook)
        notebook.add(subjects_tab, text="Subjects")
        
        self.subject_display = scrolledtext.ScrolledText(
            subjects_tab, 
            height=10, 
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.subject_display.pack(fill=tk.BOTH, expand=True, pady=5)
        self.subject_display.config(state=tk.DISABLED)  # Read-only
        
        # Subject management buttons
        subject_buttons = ttk.Frame(subjects_tab)
        subject_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            subject_buttons, 
            text="Enroll",
            command=self.enroll_subject
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            subject_buttons, 
            text="Remove",
            command=self.remove_subject
        ).pack(side=tk.LEFT, padx=5)
        
        # Profile tab
        profile_tab = ttk.Frame(notebook)
        notebook.add(profile_tab, text="Profile")
        
        # Student info
        info_frame = ttk.Frame(profile_tab, padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text=f"Name: {student.name}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Email: {student.email}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Student ID: {student.id}").pack(anchor=tk.W, pady=2)
        
        # Change password section
        password_frame = ttk.LabelFrame(profile_tab, text="Change Password", padding=10)
        password_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(password_frame, text="New Password:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.new_password_entry = ttk.Entry(password_frame, width=25, show="•")
        self.new_password_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(password_frame, text="Confirm Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.confirm_new_password_entry = ttk.Entry(password_frame, width=25, show="•")
        self.confirm_new_password_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Configure grid columns to expand
        password_frame.columnconfigure(1, weight=1)
        
        ttk.Button(
            password_frame, 
            text="Change Password", 
            command=self.change_password
        ).grid(row=2, column=0, columnspan=2, pady=10)
        
        return dashboard_frame
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        # Check for admin login
        if email == "admin@university.com" and password == "Admin123":
            self.open_admin_dashboard()
            return
        
        # Validate email format
        if not EMAIL_RE.fullmatch(email):
            messagebox.showerror("Error", "Incorrect email format.\nMust end with @university.com")
            return
        
        # Validate password format
        if not PASS_RE.fullmatch(password):
            messagebox.showerror("Error", "Incorrect password format.\nMust start with uppercase letter, have at least 5 letters and end with 3+ digits.")
            return
            
        # Search for student in database
        existing_students = self.db.load()
        logged_in_student = None
        
        for student in existing_students:
            if student.email == email and student.password == password:
                logged_in_student = student
                break
                
        if logged_in_student:
            self.current_student = logged_in_student
            self.open_student_dashboard(logged_in_student)
        else:
            messagebox.showerror("Error", "Student does not exist or credentials don't match.")
    
    def register(self):
        name = self.reg_name_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
            
        if not EMAIL_RE.fullmatch(email):
            messagebox.showerror("Error", "Incorrect email format.\nMust end with @university.com")
            return
            
        if not PASS_RE.fullmatch(password):
            messagebox.showerror("Error", "Incorrect password format.\nMust start with uppercase letter, have at least 5 letters and end with 3+ digits.")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords don't match")
            return
            
        existing_students = self.db.load()
        for s in existing_students:
            if s.email == email:
                messagebox.showerror("Error", f"Student {s.name} with email {email} already exists.")
                return
                
        try:
            new_student = Student(name=name, email=email, password=password)
            self.db.add(new_student)
            messagebox.showinfo("Success", f"Registration successful! Student ID: {new_student.id}")
            
            self.reg_name_entry.delete(0, tk.END)
            self.reg_email_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)
            self.reg_confirm_password_entry.delete(0, tk.END)
            
            self.show_frame("login")
        except ValueError as e:
            messagebox.showerror("Error", f"Registration error: {e}")
    
    def open_student_dashboard(self, student):

        if "dashboard" not in self.frames:
            self.frames["dashboard"] = self.create_dashboard_frame(student)
        else:

            self.frames["dashboard"].destroy()
            self.frames["dashboard"] = self.create_dashboard_frame(student)
        
        self.show_frame("dashboard")
        
        self.show_subjects()
    
    def logout(self):
        self.current_student = None
        
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        self.show_frame("login")
    
    def show_subjects(self):
        if not self.current_student:
            return
            
        self.subject_display.config(state=tk.NORMAL)
        self.subject_display.delete(1.0, tk.END)
        
        if not self.current_student.subjects:
            self.subject_display.insert(tk.END, "You are not enrolled in any subjects.\n")
        else:
            self.subject_display.insert(tk.END, f"Showing {len(self.current_student.subjects)} subjects:\n\n")
            
            for i, s in enumerate(self.current_student.subjects, 1):
                subject_num = s.id
                
                self.subject_display.insert(tk.END, f"{i}. Subject: ", "normal")
                self.subject_display.insert(tk.END, f"{subject_num}\n", "bold")
                
                self.subject_display.insert(tk.END, f"   Mark: {s.mark}\n", "normal")
                
                self.subject_display.insert(tk.END, f"   Grade: ", "normal")
                if s.grade == 'HD':
                    self.subject_display.insert(tk.END, f"{s.grade}\n\n", "hd")
                elif s.grade == 'D':
                    self.subject_display.insert(tk.END, f"{s.grade}\n\n", "distinction")
                elif s.grade == 'C':
                    self.subject_display.insert(tk.END, f"{s.grade}\n\n", "credit")
                elif s.grade == 'P':
                    self.subject_display.insert(tk.END, f"{s.grade}\n\n", "pass")
                else:
                    self.subject_display.insert(tk.END, f"{s.grade}\n\n", "fail")
            
            self.subject_display.insert(tk.END, "─" * 40 + "\n\n", "normal")
            
            average = self.current_student.average()
            passed = self.current_student.has_passed()
            
            self.subject_display.insert(tk.END, f"Average Mark: ", "bold")
            self.subject_display.insert(tk.END, f"{average:.2f}\n", "normal")
            
            self.subject_display.insert(tk.END, f"Overall Status: ", "bold")
            if passed:
                self.subject_display.insert(tk.END, "PASS\n", "pass_status")
            else:
                self.subject_display.insert(tk.END, "FAIL\n", "fail_status")
        
        self.subject_display.tag_configure("bold", font=("Arial", 11, "bold"))
        self.subject_display.tag_configure("normal", font=("Arial", 11))
        self.subject_display.tag_configure("hd", foreground="#9C27B0", font=("Arial", 11, "bold"))  
        self.subject_display.tag_configure("distinction", foreground="#2196F3", font=("Arial", 11, "bold"))  
        self.subject_display.tag_configure("credit", foreground="#4CAF50", font=("Arial", 11, "bold"))  
        self.subject_display.tag_configure("pass", foreground="#FFC107", font=("Arial", 11, "bold"))  
        self.subject_display.tag_configure("fail", foreground="#F44336", font=("Arial", 11, "bold"))  
        self.subject_display.tag_configure("pass_status", foreground="#4CAF50", font=("Arial", 11, "bold"))  
        self.subject_display.tag_configure("fail_status", foreground="#F44336", font=("Arial", 11, "bold"))  
        
        self.subject_display.config(state=tk.DISABLED)
    
    def enroll_subject(self):
        if not self.current_student:
            return
            
        if len(self.current_student.subjects) >= 4:
            messagebox.showerror("Error", "Students are allowed to enroll in 4 subjects only")
            return
            
        try:
            new_subject = Subject()
            self.current_student.enrol(new_subject)
            self.db.update(self.current_student)
            messagebox.showinfo("Success", f"Enrolled in {new_subject.id}\nYou are now enrolled in {len(self.current_student.subjects)} out of 4 subjects")
            self.show_subjects()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def remove_subject(self):
        if not self.current_student:
            return
            
        if not self.current_student.subjects:
            messagebox.showinfo("Information", "You are not enrolled in any subjects.")
            return
            
        remove_dialog = tk.Toplevel(self.root)
        remove_dialog.title("Remove Subject")
        remove_dialog.geometry("350x200")
        remove_dialog.resizable(False, False)
        remove_dialog.transient(self.root)
        remove_dialog.grab_set()
        
        remove_dialog.configure(bg="white")
        
        ttk.Label(remove_dialog, text="Select Subject to Remove").pack(pady=10)
        
        subjects_listbox = tk.Listbox(
            remove_dialog, 
            height=4, 
            selectmode=tk.SINGLE
        )
        subjects_listbox.pack(fill=tk.X, padx=10, pady=5)
        
        for i, s in enumerate(self.current_student.subjects):
            subject_num = s.id
            subjects_listbox.insert(tk.END, f"Subject {subject_num} - Mark: {s.mark} - Grade: {s.grade}")
        
        if self.current_student.subjects:
            subjects_listbox.selection_set(0)
        
        button_frame = ttk.Frame(remove_dialog)
        button_frame.pack(fill=tk.X, pady=10, padx=10)
        
        def do_remove():
            selection = subjects_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a subject")
                return
                
            index = selection[0]
            subject = self.current_student.subjects[index]
            subject_id = subject.id
                
            self.current_student.drop(subject_id)
            self.db.update(self.current_student)
            messagebox.showinfo("Success", f"Dropped {subject_id}")
            remove_dialog.destroy()
            self.show_subjects()
        
        ttk.Button(
            button_frame, 
            text="Remove",
            command=do_remove,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancel",
            command=remove_dialog.destroy,
            width=10
        ).pack(side=tk.RIGHT, padx=5)
    
    def change_password(self):
        if not self.current_student:
            return
            
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_new_password_entry.get()
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords don't match")
            return
            
        try:
            self.current_student.change_password(new_password)
            self.db.update(self.current_student)
            
            self.new_password_entry.delete(0, tk.END)
            self.confirm_new_password_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Password changed successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def open_admin_dashboard(self):
        if "admin_dashboard" not in self.frames:
            self.frames["admin_dashboard"] = self.create_admin_dashboard()
        
        self.show_frame("admin_dashboard")
        
        self.show_all_students()
        
def run_university_app():
    root = tk.Tk()
    app = UniversityApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    run_university_app() 