students = []
grades = []


def add_student(name, age):
    student_id = len(students) + 1
    students.append({"id": student_id, "name": name, "age": age})
    grades.append({"student_id": student_id, "scores": []})


def add_grade(student_name, score):
    student_info = next(
        (student for student in students if student["name"] == student_name), None
    )
    if student_info:
        student_id = student_info["id"]
        for g in grades:
            if g["student_id"] == student_id:
                g["scores"].append(score)
                break
    else:
        print(f"找不到学生 {student_name}")


def show_all_students():
    for student in students:
        print(f"ID: {student['id']}, 姓名: {student['name']}, 年龄: {student['age']}")


def get_student_grades(student_name):
    for student in students:
        if student["name"] == student_name:
            student_id = student["id"]
            break
    else:
        print(f"找不到学生 {student_name}")
        return []

    for g in grades:
        if g["student_id"] == student_id:
            return g["scores"]
    return []


def calculate_student_average(student_name):
    scores = get_student_grades(student_name)
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def calculate_class_average():
    total = 0
    count = 0
    for g in grades:
        total += sum(g["scores"])
        count += len(g["scores"])
    if count == 0:
        return 0.0
    return total / count


# 测试数据
add_student("张三", 20)
add_student("李四", 22)

add_grade("张三", 85)
add_grade("张三", 90)
add_grade("李四", 78)
add_grade("李四", 88)

print("所有学生信息：")
show_all_students()

print("\n各学生成绩：")
print(f"张三的成绩: {get_student_grades('张三')}")
print(f"李四的成绩: {get_student_grades('李四')}")

print("\n计算平均分：")
print(f"张三平均分: {calculate_student_average('张三'):.2f}")  # 修复后的结果
print(f"李四平均分: {calculate_student_average('李四'):.2f}")  # 修复后的结果
print(f"全年级平均分: {calculate_class_average():.2f}")
