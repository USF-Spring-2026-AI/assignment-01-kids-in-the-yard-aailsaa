# AI Assignment 01 - Kids in the Yard

Comparison:

● Which tool(s) did you use?
    I used cursor with the auto model selection setting, so it switches between models.

● If you used an LLM, what was your prompt to the LLM?
    I prompted it a few times but in the most successful attempt I gave it the full spec doc provided and the prompt message:
    "please read the implementation of kids running in the yard pdf and create the family tree application. make sure to generate people using the statistics provided in csvs, and separate this program into different objects as sugested by the doc. Please write this like a professional software engineer."

● What differences are there between your implementation and the LLM?
    One main difference between implementations is the organization from the LLM. putting all of the code in a src directory and creating a requirements.txt file are a few examples of how the LLM had a more organized and sophisticated implimentation. 
    My most recent LLM generated implementation is similarly structured with person and tree classes, but all previous attempts tried to generate everything in a single file with as few methods and classes as possible. This was a big difference from my implimentation and what I was expecting.

● What changes would you make to your implementation in general based on suggestions from the
LLM?
    I would add more organization to my repo, and comment more in the python style. In general visibility is something I took away from the LLM representation.

● What changes would you refuse to make?
    I would keep the consts that I use throughout my code. I dont see the LLM implementation using any const values in all uppercase, and I like the way they're easy to find and don't change in value. 

