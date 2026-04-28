import os
import csv
import json

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def check_file(self):
        if os.path.exists(self.file_path):
            return True
        return False

    def create_output_folder(self, folder="output"):
        if not os.path.exists(folder):
            os.makedirs(folder)

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.students = []

    def load(self):
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.students.append(row)
        except:
            pass

    def preview(self, n=5):
        for row in self.students[:n]:
            print(f"{row['student_id']} | {row['country']} | GPA: {row['GPA']}")

class DataAnalyser:
    def __init__(self, data):
        self.data = data
        self.result = {}

    def analyse(self):
        counts = {}
        for s in self.data:
            country = s["country"]
            counts[country] = counts.get(country, 0) + 1
        
        sorted_countries = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        top_3 = sorted_countries[:3]

        self.result = {
            "variant": "B",
            "total_students": len(self.data),
            "top_3_countries": top_3,
            "all_statistics": counts
        }

    def print_results(self):
        print("Analysis completed.")

class ResultSaver:
    def __init__(self, data, path):
        self.data = data
        self.path = path

    def save_json(self):
        try:
            with open(self.path, "w", encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except:
            pass

def main():
    INPUT = "students.csv"
    OUTPUT = "output/result.json"

    fm = FileManager(INPUT)
    if not fm.check_file():
        return
    fm.create_output_folder()

    dl = DataLoader(INPUT)
    dl.load()
    dl.preview()

    high_gpa = list(filter(lambda x: float(x["GPA"]) > 3.9, dl.students))
    print(f"Filtered: {len(high_gpa)}")

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result, OUTPUT)
    saver.save_json()

if __name__ == "__main__":
    main()