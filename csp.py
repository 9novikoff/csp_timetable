from math import factorial
import constraint
from itertools import product, permutations
from sympy.utilities.iterables import multiset_permutations
import matplotlib.pyplot as plt

def visualize_timetable(timetable):
    days = 5
    groups = list(timetable.keys())

    fig, ax = plt.subplots()

    ax.axis('off')

    table_data = []

    for day in range(days):
        for subject_number in range(max_subjects_per_day):
            table_data.append([timetable[group][day*5 + subject_number][0] + ' ' + timetable[group][day*5 + subject_number][1] if timetable[group][day*5 + subject_number] != '' else '' for group in groups])

    row_labels = [f"subject {subject} day {day}" for subject in range(1, days+1) for day in range(1, max_subjects_per_day+1)]

    table = ax.table(cellText=table_data, colLabels=groups, loc='center', cellLoc='center', rowLabels=row_labels)

    plt.show()

def get_permutation_by_index(lst, index):
    n = len(lst)
    permutation = list(range(1, n + 1)) 
    
    for i in range(n - 1, 0, -1):
        factorial_value = factorial(i)
        selected_index = index // factorial_value
        permutation[i], permutation[i - selected_index] = permutation[i - selected_index], permutation[i]
        index %= factorial_value

    result = [lst[i - 1] for i in permutation]
    return result

def find_similar_teachers(teacher, subjects_constraint):
    similar_teachers = []
    subjects_taught = set(subjects_constraint.get(teacher, []))

    for other_teacher, subjects in subjects_constraint.items():
        if other_teacher != teacher and any(subject in subjects_taught for subject in subjects):
            similar_teachers.append(other_teacher)

    return similar_teachers

                
def balance_teachers(groups_subjects_permutation, teacher, subjects_constraint, groups, teachers, unit, teachers_base):
  helpers = [t for t in find_similar_teachers(teacher, subjects_constraint) if t not in teachers_base]
  for helper in helpers:
    if teachers[helper] > 0:
      for group in groups:
        for i in range(unit):
          groups_subjects_permutation[group][i][0]
              
             

def generate_all(subjects_constraint, group_constraint, teacher_constraint, subject_per_day, days):
    teachers = teacher_constraint.copy()
    groups_subjects_permutation = {}
    for group in group_constraint.keys():
      group_subjects_permutation = []
      for group_subject in group_constraint[group].keys():
        for i in range(group_constraint[group][group_subject]):
          teacher = sorted([[teacher, teachers[teacher]] for teacher in subjects_constraint[group_subject]], key=lambda x: x[1], reverse=True)[0][0]         
          group_subjects_permutation.append([group_subject, teacher])
          teachers[teacher] -= 1
      for empty in range(subject_per_day*days - len(group_subjects_permutation)):
        group_subjects_permutation.append("")
      groups_subjects_permutation[group] = group_subjects_permutation
    return groups_subjects_permutation

def find_optimal_schedule(groups_subjects_permutation, subjects_constraint, teacher_constraint, group_constraint):
  teachers = teacher_constraint.copy()
  groups = list(group_constraint.keys())
  groups_permutation = {group_i: 0 for group_i in range(len(groups))}
  unit = 0
  while unit != len(groups_subjects_permutation[groups[0]]):
    group_i = 0
    group_j = 0
    while group_i < len(group_constraint.keys()):
      while group_j < group_i:
        if(groups_subjects_permutation[groups[group_i]][unit] != '' and groups_subjects_permutation[groups[group_j]][unit] != '' and
             groups_subjects_permutation[groups[group_i]][unit][1] == groups_subjects_permutation[groups[group_j]][unit][1]):
          max_index = max(group_i, group_j)
          while(groups_subjects_permutation[groups[group_i]][unit] != '' and groups_subjects_permutation[groups[group_j]][unit] != '' and
             groups_subjects_permutation[groups[group_i]][unit][1] == groups_subjects_permutation[groups[group_j]][unit][1]):
            groups_permutation[max_index] += 1
            permutation = get_permutation_by_index(groups_subjects_permutation[groups[max_index]][unit:], groups_permutation[max_index])
            groups_subjects_permutation[groups[max_index]][unit:] = permutation
          group_j = 0
        else:
          group_j += 1
      if(groups_subjects_permutation[groups[group_i]][unit] != ''):
        if(teachers[groups_subjects_permutation[groups[group_i]][unit][1]] <= 0):
          change = sorted([[teacher, teachers[teacher]] for teacher in subjects_constraint[groups_subjects_permutation[groups[group_i]][unit][0]]], key=lambda x: x[1], reverse=True)[0]
          if(change[1] <= 0):
            teachers[groups_subjects_permutation[groups[group_i]][unit][1]] -= 1
          else:
            teachers[change[0]] -= 1
            groups_subjects_permutation[groups[group_i]][unit][1] = change[0]
        else:
          teachers[groups_subjects_permutation[groups[group_i]][unit][1]] -= 1
      group_i += 1
      group_j = 0
    groups_permutation = {group_i: 0 for group_i in range(len(groups))}
    unit += 1
  return teachers, groups_subjects_permutation

subjects_constraint = {
    'linalg': ['teacher1', 'teacher2'],
    'calculus': ['teacher1', 'teacher3'],
    'db': ['teacher3'],
    'english': ['teacher6'],
    'stats': ['teacher4', 'teacher5'],
    'ai': ['teacher4', 'teacher5']
}

group_constraint = {
    'tk': {'linalg': 3, 'calculus': 2, 'db': 3, 'english': 2, 'stats': 2, 'ai': 3},
    'mi': {'linalg': 3, 'calculus': 4, 'db': 3, 'english': 1, 'stats': 5, 'ai': 1},
    'ttp': {'linalg': 3, 'calculus': 3, 'db': 3, 'english': 2, 'stats': 2, 'ai': 1}
}

teacher_constraint = {
    'teacher1': 13,
    'teacher2': 8,
    'teacher3': 15,
    'teacher4': 7,
    'teacher5': 7,
    'teacher6': 5
}

days = 5
max_subjects_per_day = 5


s = generate_all(subjects_constraint, group_constraint, teacher_constraint, max_subjects_per_day, days)

remain, solution = find_optimal_schedule(s, subjects_constraint, teacher_constraint, group_constraint)

print(remain)
visualize_timetable(solution)

