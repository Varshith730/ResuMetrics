from fpdf import FPDF

pdf = FPDF()
pdf.add_page("P")
pdf.set_font("Arial", size=10)

text = """GUNDA BATTU VARSHITH RAJU
Senior Data Scientist & Machine Learning Architect
Email: gundabattu@gmail.com | LinkedIn: linkedin.com/in/varshith | Phone: +1-555-0123

PROFESSIONAL SUMMARY
Highly accomplished and results-driven Senior Data Scientist with 9+ years of experience spearheading advanced machine learning initiatives, delivering models that achieve over 99% accuracy across highly distributed systems. 

TECHNICAL SKILLS
* Data Science: Statistics, NLP, Data Science, mathematical modeling
* Machine Learning: Machine Learning, Deep Learning, scikit-learn, sklearn, TensorFlow, PyTorch, Keras, xgboost
* Programming: Python, Java, JavaScript, TypeScript, Go, C++, SQL, PostgreSQL, MongoDB
* Cloud & DevOps: AWS, Azure, GCP, Docker, Kubernetes, Terraform, agile, CI/CD, Git, Github Actions

PROFESSIONAL EXPERIENCE
Senior Data Scientist | Softways IT Solutions (2018 - Present)
* Directed predictive models using deep learning and tensorflow, resulting in a 45% enhancement in classification efficacy.
* Re-engineered and optimized critical neural network pipelines with pytorch, decreasing model training latency by over 30%.
* Systematically analyzed and processed over 150M+ rows of complex SQL data, generating mission-critical statistics for core business KPIs.
* Initiated a rigorous training program, mentoring 12+ junior data analysts, boosting team output by 35%.
* Published 3 peer-reviewed whitepapers on novel applications of natural language processing.
* Successfully transitioned 14 legacy statistical models into a modern, containerized machine learning ecosystem leveraging docker and kubernetes.

Machine Learning Engineer | DataCorp Logistics (2015 - 2018)
* Programmed sophisticated time-series forecasting algorithms that predicted global supply chain delays with an unprecedented 94% accuracy.
* Architected a real-time anomaly detection system utilizing python and spark to isolate fraudulent transactions, preventing over $2M in annual losses.
* Collaborated closely with devops teams to establish continuous delivery frameworks, reducing deployment cycles by 60%.
* Automated the ingestion of unstructured data into clean data lakes using aws and airflow.
* Delivered 10+ presentations to C-level executives detailing ROI of advanced analytics.

ACADEMIC BACKGROUND
B.Tech Computer Science & Engineering | SR University (2011 - 2015)
* Specialized in Artificial Intelligence, Statistical Modeling, and Database Systems.

MAJOR PROJECTS & IMPLEMENTATIONS
Smart Pregnancy Monitoring with AI Assistance
* Designed a classification model yielding 95% accuracy in early-stage diagnostics.
* Engineered a continuous training pipeline leveraging tensorflow, reducing computation workflows by 40%.
* Secured 1st place in a national healthcare hackathon against 200+ competing engineering teams.

e-Swasthi AI Mental Health Platform
* Created an advanced natural language processing (nlp) sentiment analysis engine capable of predicting behavioral shifts with 92% precision.
* Handled over 1.5M+ daily API requests via a highly optimized inference service.
"""

pdf.multi_cell(0, 5, text)
pdf.output("Varshith_Data_Scientist_Resume.pdf")
print("ULTIMATE RESUME PDF GENERATED")
