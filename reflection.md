# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  consists of a Owner that owns 0 or more pets, and each pet has its own attributes, and has 0 or more tasks

- What classes did you include, and what responsibilities did you assign to each?
  - Owner
    - can add or edit pets
    - can add or edit tasks
  - Pet
    - has name, corresponding tasks
  - Task
    - has priority of different tasks
    - displays duration 

**b. Design changes**

- Did your design change during implementation?
  - Yes
- If yes, describe at least one change and why you made it.
  - in `Task` a description field was added. Now we can distinguised each task. 
  - in `Task` identification was added
  - updated `editPet` signature
  - updated `duration` in `Task` 
  - 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - Conflict detection compares every pair of tasks instead of using a faster sweep-line algorithm that sorts tasks and tracks overlapping intervals in one pass. The pairwise approach is O(n^2) a sweep-line would be O(n log n).
- Why is that tradeoff reasonable for this scenario?
    - PawPal+ schedules tasks for one owner's pets, so the task list is small (not thousands). At that scale the O(n^2) difference is unnoticeable, and the pairwise comparison is much simpler to read and verify than a sweep-line implementation.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
