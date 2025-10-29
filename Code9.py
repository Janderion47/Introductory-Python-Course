class Patient:
    def __init__(self,n,a,g,bp,t):
        self.name = n
        self.age = a
        self.gender = g
        self.bloodpressure = bp # Bp as a pair of (systolic, diastolic)
        self.temperature = t
    
    def display_patient_info(self):
        return(
            f"Name: {self.name}\n"
            f"Age: {self.age}\n"
            f"Gender: {self.gender}\n"
            f"Blood Pressure: {self.bloodpressure}\n"
            f"Temperature: {self.temperature}"
            )
    
    def is_hypertensive(self):
        sys, dia = self.bloodpressure
        return sys>=140 or dia>=90
    
    def is_feverish(self):
        return self.temperature >= 37.5


if __name__ == "__main__":
    pat1 = Patient("John Doe",45,"Male", (140,85), 36.8)
    pat2 = Patient("Jane Smith", 32, "Female", (130,88), 37.6)
    
    print("Patient 1 Information:")
    print(pat1.display_patient_info(),end="\n\n")
    
    print("Patient 2 Information:")
    print(pat2.display_patient_info(),end="\n\n")
