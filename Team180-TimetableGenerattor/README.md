#Buffer 7.0 project
##Team Members 
- Shewale Asmita
- Vaishampayan Dhanashree


 Problem statement: 
Creating a lecture timetable manually can be time-consuming and error-prone. Teachers and students often face overlapping classes, some subjects don’t get enough periods, and too many lectures in a day can make schedules chaotic. The goal of this project is to build a system that can automatically generate a balanced timetable, making sure lectures don’t overlap, every subject gets the required hours, and daily schedules stay manageable. This will use data structures and algorithms to solve the problem efficiently for both classes and teachers. 
Description of data structures used: 
Dictionary (for classes, teachers, subjects): used for fast lookup and organized mapping (e.g., class → timetable, teacher → availability). 
2D List (matrix): used to represent the timetable as days × slots, making it easy to access and update any position directly. 
Nested Dictionary (subject count): used to track how many times each subject is assigned, ensuring required hours are met. 
2D Boolean List (teacher availability): used to quickly check if a teacher is free or busy at a given time slot. 
Greedy + Random approach: used to assign slots efficiently while trying to satisfy constraints without heavy computation. 
Constraint checking logic: ensures no clashes, no repetition, and balanced scheduling. 
Limited attempts (loop control): prevents infinite loops and keeps the algorithm efficient. 

1. Backend Logic 
Uses dictionary (hash map) to store timetable → fast access using class name 
Uses 2D lists for each class → represents days × slots structure 
Uses random allocation to assign subjects → avoids fixed/manual scheduling 
Uses constraint checking: ○ Teacher availability (teacher_busy) 
   No slot clash 
   No consecutive same subject 
  Max 2 lectures per subject per day 

Uses loop + attempts limit (500) → prevents infinite loops 
Uses fallback logic → fills remaining slots if constraints fail 
Uses modulus (%) to assign teachers to subjects cyclically 

 2. Input 
From UI (user enters): 
  Classes (A, B, C…) 
   Subjects 
   Teachers 
   Hours per subject 
    Days (Mon, Tue…) 
 Number of slots per day 

 3. Output 
 Timetable (dictionary format internally) 
 GUI display (tab-wise for each class using table layout) 
 CSV files for each class 
 Visual output: ○ Free slots highlighted 
 Subject + Teacher shown in each cell 
#Demo Video Link
https://drive.google.com/file/d/1Q7rCmfMgquYr9nKYxOTMc4zXalFk51C-/view?usp=drive_link
