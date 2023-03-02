# TA-Assignments
Utilizes evolutionary computing and functional programming to assign teaching assistants to course sections in a way that satisfies both the teaching assistants' preferences (number of days assigned, times of assignment, etc.) and the instructors' preferences (minimum number of TAs in a section, times of the section, etc.)

Objectives driving evolutionary processes:
1) Minimize overallocation of TAs (assigning TAs to more sections than they are willing to take on)
2) Minimize time conflicts (assigning TAs to sections happening simultaneously)
3) Minimize Under-Support (not assigning enough TAs to a section)
4) Minimize the number of times you allocate a TA to a section they are unwilling to support 
5) Minimize the number of times you allocate a TA to a section where they said “willing” but not “preferred”

Agents driving evolutionary process:
1) assign_preferred(): assigns each TA to their preferred sections
2) fix_unwilling(): unassigns each TA from sections they are unwilling to take on
3) fix_unpreferred(): unassigns each TA from sections that are not preferred
4) fix_overassignment(): ensures TAs are not teaching more sections than they are willing to
5) fix_undersupport(): ensures sections are being supported by enough TAs

To begin the evolutionary process for this task, run the "assign_tas.py" file.
