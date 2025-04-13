# JULIUS BÄR
# Onboard Quest - Improve Client Onboarding Efficiency in Private Banking using Machine Learning and Gamification

Welcome to our **SwissHacks25** project — a compliance-driven automation tool developed for Julius Bär. This solution is designed to support Relationship Managers and compliance officers by systematically verifying that all client onboarding requirements are fulfilled in accordance with regulatory and internal policies.

## Introduction:

#### What is the current problem?
In private banking, the onboarding process requires verifying client information against a set of regulatory rules to ensure compliance. This manual process is often time-consuming and error-prone, leading to delays and a poor customer experience. Inconsistencies in documentation represent another major challenge. Onboarding can involve analysing 200-300 pages of information and contracts, where discrepancies are not only common but also significantly impact efficiency. Document and data analysis may seem mundane, but the pain today is substantial. 

#### What is the expected final product?
The expectation is to develop an automated solution that can support Relationship Managers and compliance functions to ensure all onboarding rules are duly met during client onboarding.

#### Who are the users of this solution?
* Relationship Managers
* Compliance functions (1st line of defense) 

#### Use Case: 
* There is a lot of back and forth between RM and clients and risk employees, so we want to improve the efficiency of the client onboarding via an automated solution. 

### Expected Outcome:

The expectation is to develop an automated solution that can support Relationship Managers and compliance functions to ensure all onboarding rules are duly met during client onboarding, enhanced with gamification elements so the journey is efficient and more entertaining. 

## Installation of the Repository
Step-by-step instructions on how to get the tool environment running.

- **Clone the repository**
```bash
git clone https://github.com/Licates/juliusbaer.git
```

- **Navigate to the project directory**
```bash
cd juliusbaer
```

- **Create and activate the environment**
```bash
pip install -r requirements.txt
```

## Using our Tool
Decide between webinterface or game

```bash
pip install -r requirements.txt
```

### Manual (Command Line)

Run this command to start the program and communicate with the Julius Bär API.
```bash
python3 main.py
```

### Tool Output
The tool returns the following details for each analysis:

- **Score**  
  Current streak of correct decisions (e.g., `Current score: 1`).  

- **Model Result**  
  AI’s consistency verdict (e.g., `Gemini result: FALSE`).  

- **Decision Logic**  
  Brief explanation of the analysis (e.g., `"All core identity fields are consistent..."`).  

- **API Key**  
  The key used for the request (e.g., `Using API key: XXXXX`).  

- **Final Decision**  
  `Accept` (documents consistent) or `Reject` (inconsistencies detected).

### Web Interface
The application launches a web interface where you can drag and drop files to process them. This is a proof-of-concept demo and needs integration into the target project.

![Slide 1](/slides/tool1.jpeg)
![Slide 2](/slides/tool2.jpeg)


## The Pitch:

Insert Pitchdeck here
![Slide 1](/slides/slide1.png)
![Slide 2](/slides/slide2.png)

## Deep Dive Slides:

Insert Deep Dive Slides here:
![Slide 1](/slides/slide1.png)
![Slide 2](/slides/slide2.png)

## Further Information:
### API Key Distribution
Each participating team will receive a unique API key.

### Initial Request
Teams will use the API key to send an initial request to the designated endpoint, which will respond with a set of four documents:  
- Passport (png)  
- Client Profile (docx)  
- Account Opening Form (pdf)  
- Client Description (txt)

### Document Analysis
Teams must analyze the contents of these documents to determine if they are consistent with each other. Consistency will be evaluated based on predefined criteria (e.g., matching names, addresses, dates of birth, etc.).

### Response Submission
After analyzing the documents, teams must submit a response indicating whether the documents are consistent ("Accept") or not ("Reject").

### Game Progression
If the submitted response is correct, the team will receive a new set of documents for analysis. If the response is incorrect, the game will restart from the beginning.

### Scorekeeping
For each API key, the system will track the longest sequence of correct responses (i.e., the "session"). The team with the longest session at the end of the challenge will be considered the winner.

## Resources:
Frontend - register your team with given API key at following URL: https://hackathon-frontend.mlo.sehlat.io/  
Backend - check specification of endpoints at following URL: https://hackathon-api.mlo.sehlat.io/docs

#### Important Technologies: 


## Judging Criteria:
* Efficiency gain: Solution improves the efficiency, simplifies the process and adds some value to the step when it comes to documentation of the onboarding process
* Longest session: Team that will have the longest session in the game receive extra credits

## Point of Contact:

*	Claudine / Senad will be present and in Jury
*	The sponsor: Compliance: Tech: also, during the wknd 
*	front risk employees will be involved
*	HR reps for the booth during the wknd


## Price - the winning team members will each receive:

Inviation to Julius Bär premises to present their solution in front of senior management and potential stakeholders.
