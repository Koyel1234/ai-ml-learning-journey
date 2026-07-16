import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime

# Create directory
directory_name = "ai"
os.makedirs(directory_name, exist_ok=True)
print(f"Directory '{directory_name}' created/verified at current location.")

# Define common styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=20,
    alignment=1
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2e5c8a'),
    spaceAfter=12,
    spaceBefore=12
)

# PDF 1: Machine Learning Basics
def create_ml_basics():
    pdf_path = os.path.join(directory_name, "machine_learning_basics.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    
    # PAGE 1
    elements.append(Paragraph("Machine Learning Basics", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    page1_content = [
        ("What is Machine Learning?", 
         "Machine Learning is a subset of Artificial Intelligence that enables systems to learn and improve from experience without being explicitly programmed. Instead of following explicit instructions, ML systems learn patterns from data."),
        
        ("Types of Machine Learning",
         "1. <b>Supervised Learning:</b> Learning with labeled data (e.g., Classification, Regression)<br/>"
         "2. <b>Unsupervised Learning:</b> Learning patterns from unlabeled data (e.g., Clustering, Dimensionality Reduction)<br/>"
         "3. <b>Reinforcement Learning:</b> Learning through interaction and rewards"),
        
        ("Applications of Machine Learning",
         "• Email spam filtering<br/>"
         "• Recommendation systems<br/>"
         "• Fraud detection<br/>"
         "• Image recognition<br/>"
         "• Natural language processing<br/>"
         "• Predictive analytics")
    ]
    
    for heading, text in page1_content:
        elements.append(Paragraph(heading, heading_style))
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
    
    # PAGE BREAK
    elements.append(PageBreak())
    
    # PAGE 2
    elements.append(Paragraph("ML Algorithms & Techniques", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    page2_content = [
        ("Key Algorithms",
         "<b>Regression Algorithms:</b><br/>"
         "• Linear Regression<br/>"
         "• Logistic Regression<br/>"
         "• Ridge & Lasso Regression<br/><br/>"
         "<b>Tree-based Algorithms:</b><br/>"
         "• Decision Trees<br/>"
         "• Random Forest<br/>"
         "• Gradient Boosting<br/><br/>"
         "<b>Clustering Algorithms:</b><br/>"
         "• K-Means<br/>"
         "• Hierarchical Clustering<br/>"
         "• DBSCAN"),
        
        ("Distance & Similarity Metrics",
         "• Euclidean Distance<br/>"
         "• Manhattan Distance<br/>"
         "• Cosine Similarity<br/>"
         "• Hamming Distance"),
        
        ("Cross-Validation Techniques",
         "• K-Fold Cross-Validation<br/>"
         "• Stratified K-Fold<br/>"
         "• Time Series Split")
    ]
    
    for heading, text in page2_content:
        elements.append(Paragraph(heading, heading_style))
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
    
    # PAGE BREAK
    elements.append(PageBreak())
    
    # PAGE 3
    elements.append(Paragraph("ML Workflow & Best Practices", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    page3_content = [
        ("Steps in Machine Learning Pipeline",
         "1. <b>Data Collection:</b> Gather relevant data<br/>"
         "2. <b>Data Preprocessing:</b> Clean and prepare data<br/>"
         "3. <b>Exploratory Data Analysis (EDA):</b> Understand data patterns<br/>"
         "4. <b>Feature Engineering:</b> Create meaningful features<br/>"
         "5. <b>Model Selection:</b> Choose appropriate algorithm<br/>"
         "6. <b>Model Training:</b> Fit model to training data<br/>"
         "7. <b>Model Evaluation:</b> Assess performance<br/>"
         "8. <b>Hyperparameter Tuning:</b> Optimize model parameters<br/>"
         "9. <b>Deployment:</b> Put model into production"),
        
        ("Performance Metrics",
         "<b>For Regression:</b><br/>"
         "• Mean Absolute Error (MAE)<br/>"
         "• Mean Squared Error (MSE)<br/>"
         "• R-squared (R²)<br/><br/>"
         "<b>For Classification:</b><br/>"
         "• Accuracy<br/>"
         "• Precision & Recall<br/>"
         "• F1-Score<br/>"
         "• ROC-AUC"),
        
        ("Common Challenges",
         "• Overfitting: Model memorizes training data<br/>"
         "• Underfitting: Model too simple for data<br/>"
         "• Class Imbalance: Unequal class distribution<br/>"
         "• Feature Scaling: Normalize feature values<br/>"
         "• Missing Data: Handle incomplete records")
    ]
    
    for heading, text in page3_content:
        elements.append(Paragraph(heading, heading_style))
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
    
    doc.build(elements)
    print(f"✓ Created: {pdf_path} (3 pages)")

# PDF 2: Deep Learning Fundamentals
def create_deep_learning():
    pdf_path = os.path.join(directory_name, "deep_learning_fundamentals.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    
    elements.append(Paragraph("Deep Learning Fundamentals", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    content = [
        ("What is Deep Learning?",
         "Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers to model complex patterns in data."),
        
        ("Neural Network Architecture",
         "<b>Components:</b><br/>"
         "• Input Layer: Receives data<br/>"
         "• Hidden Layers: Process information<br/>"
         "• Output Layer: Produces predictions<br/>"
         "• Weights & Biases: Learnable parameters"),
        
        ("Common Deep Learning Models",
         "• <b>Convolutional Neural Networks (CNN):</b> For image processing<br/>"
         "• <b>Recurrent Neural Networks (RNN):</b> For sequential data<br/>"
         "• <b>Long Short-Term Memory (LSTM):</b> For long sequences<br/>"
         "• <b>Transformers:</b> For NLP and attention mechanisms"),
        
        ("Activation Functions",
         "• ReLU (Rectified Linear Unit)<br/>"
         "• Sigmoid<br/>"
         "• Tanh<br/>"
         "• Softmax"),
        
        ("Popular Frameworks",
         "• TensorFlow<br/>"
         "• PyTorch<br/>"
         "• Keras")
    ]
    
    for heading, text in content:
        elements.append(Paragraph(heading, heading_style))
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
    
    doc.build(elements)
    print(f"✓ Created: {pdf_path}")

# PDF 3: Generative AI & LLMs
def create_genai_llms():
    pdf_path = os.path.join(directory_name, "generative_ai_llms.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    
    elements.append(Paragraph("Generative AI & Large Language Models (LLMs)", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    content = [
        ("What is Generative AI?",
         "Generative AI refers to AI systems that can generate new content such as text, images, audio, and code based on learned patterns from training data."),
        
        ("Large Language Models (LLMs)",
         "<b>Definition:</b> LLMs are deep learning models trained on massive amounts of text data to understand and generate human language.<br/><br/>"
         "<b>Capabilities:</b><br/>"
         "• Text generation<br/>"
         "• Question answering<br/>"
         "• Translation<br/>"
         "• Summarization<br/>"
         "• Code generation"),
        
        ("Popular LLMs",
         "• OpenAI's GPT Series (GPT-3.5, GPT-4)<br/>"
         "• Google's Bard/PaLM<br/>"
         "• Meta's LLaMA<br/>"
         "• Anthropic's Claude"),
        
        ("Transformer Architecture",
         "LLMs use Transformer architecture which includes:<br/>"
         "• Self-Attention Mechanism<br/>"
         "• Multi-Head Attention<br/>"
         "• Positional Encoding<br/>"
         "• Feed-Forward Networks"),
        
        ("Applications",
         "• Chatbots and Virtual Assistants<br/>"
         "• Content Generation<br/>"
         "• Code Assistance<br/>"
         "• Research and Analysis<br/>"
         "• Customer Support")
    ]
    
    for heading, text in content:
        elements.append(Paragraph(heading, heading_style))
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
    
    doc.build(elements)
    print(f"✓ Created: {pdf_path}")

# Create all PDFs
if __name__ == "__main__":
    try:
        create_ml_basics()
        create_deep_learning()
        create_genai_llms()
        print(f"\n✓ All PDFs created successfully in '{directory_name}/' directory!")
    except Exception as e:
        print(f"Error: {e}")
