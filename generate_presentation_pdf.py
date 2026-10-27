import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' in footer,
    along with a running header.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages after title page)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "ReSumo — Project Presentation & Viva Defense Guide")
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "Team Study & Presentation Document")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * 72 - 54, 45)
        self.drawString(54, 32, "Confidential — Prepared for Academic Capstone & Team Presentation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 32, page_str)
        self.restoreState()


def create_presentation_pdf(output_filename="ReSumo_Project_Presentation_Guide.pdf"):
    # Margins: 0.75 in (54 pt)
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Navy
    ACCENT = colors.HexColor("#2563EB")     # Bright Royal Blue
    TEXT_DARK = colors.HexColor("#1E293B")  # Dark Slate
    TEXT_MUTED = colors.HexColor("#64748B") # Muted Gray
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Light Slate
    BORDER_COLOR = colors.HexColor("#CBD5E1") # Border Gray
    GREEN_ACCENT = colors.HexColor("#059669") # Emerald Green
    AMBER_ACCENT = colors.HexColor("#D97706") # Amber

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceAfter=15,
    )

    meta_style = ParagraphStyle(
        "DocMeta",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=TEXT_MUTED,
        spaceAfter=15,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6,
    )

    body_bold = ParagraphStyle(
        "BodyDarkBold",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletItem",
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
    )

    def make_box(content_flowables, bg=BG_LIGHT, border=ACCENT):
        tbl = Table([[content_flowables]], colWidths=[504])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("BOX", (0, 0), (-1, -1), 1, border),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        return tbl

    elements = []

    # ==================== COVER / HEADER ====================
    elements.append(Paragraph("ReSumo 🚀", title_style))
    elements.append(Paragraph("AI-Driven Recruitment & Onboarding Automation Platform", subtitle_style))
    elements.append(Paragraph(
        "<b>Team Presentation & Viva Defense Master Guide</b> | Simple English Reference Manual<br/>"
        "<i>Includes All AI Models, Training Datasets, Full Tech Stack, Architecture & 10 Model Viva Answers</i>",
        meta_style
    ))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=14))

    # ==================== SECTION 1: THE 30-SECOND PITCH ====================
    elements.append(Paragraph("1. The 30-Second Elevator Pitch (How to Open Your Talk)", h1_style))
    pitch_text = (
        "<b>Speak this verbatim with confidence:</b><br/>"
        "<i>'Good morning everyone. Today we are presenting <b>ReSumo</b> — an AI-powered talent acquisition "
        "and onboarding automation platform. Traditional recruiting is slow, keyword-dependent, and prone to human bias. "
        "ReSumo solves this by combining a <b>fine-tuned 20B LLM for structured resume parsing</b>, <b>dense vector embeddings for semantic matching</b>, "
        "and a <b>Human-in-the-Loop tiered approval engine</b>. It automates everything from resume upload and RAG matching to "
        "AI interview scorecards, formal offer letters, and digital employee onboarding.'</i>"
    )
    elements.append(make_box(Paragraph(pitch_text, callout_style), bg=colors.HexColor("#EFF6FF"), border=ACCENT))
    elements.append(Spacer(1, 10))

    # ==================== SECTION 2: PROBLEM & SOLUTION ====================
    elements.append(Paragraph("2. Problem Statement & ReSumo's Solution", h1_style))
    prob_table_data = [
        [Paragraph("Traditional Hiring Pain Point", table_header_style), Paragraph("How ReSumo Solves It", table_header_style)],
        [
            Paragraph("<b>Keyword Search Fails:</b> Looking for 'FastAPI' ignores candidates who wrote 'Python async microservices'.", table_cell_style),
            Paragraph("<b>Semantic RAG Vector Matching:</b> Uses 1,024-dimension embeddings to understand the <i>meaning</i> of skills, not just spelling.", table_cell_style)
        ],
        [
            Paragraph("<b>Complex Resume Layouts:</b> Tables, multiple columns, and varied styles break traditional regex parsers.", table_cell_style),
            Paragraph("<b>Fine-Tuned LLM (QLoRA):</b> Trained on 5,000 resumes to extract 15 exact structured JSON fields with zero formatting failure.", table_cell_style)
        ],
        [
            Paragraph("<b>Fear of Black-Box AI Bias:</b> Fully automated hiring can lead to compliance violations and unfair rejections.", table_cell_style),
            Paragraph("<b>Human-In-The-Loop (HITL):</b> AI provides scores and written rationales, but human managers must officially approve each promotion.", table_cell_style)
        ],
        [
            Paragraph("<b>Disconnected Tools:</b> Companies switch between 5 different tools for jobs, interviews, offers, and onboarding.", table_cell_style),
            Paragraph("<b>Unified Single Platform:</b> Covers the complete hiring pipeline: Sourcing → Matching → Approvals → Interviews → Offers → Onboarding.", table_cell_style)
        ],
    ]
    t_prob = Table(prob_table_data, colWidths=[240, 264])
    t_prob.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_prob)
    elements.append(Spacer(1, 14))

    # ==================== SECTION 3: ALL AI MODELS USED ====================
    elements.append(PageBreak())
    elements.append(Paragraph("3. Deep Dive: All AI & Machine Learning Models Used", h1_style))
    elements.append(Paragraph(
        "Examiners always ask detailed questions about the AI components. ReSumo utilizes <b>4 specialized AI/ML models</b>:",
        body_style
    ))

    # Model 1
    elements.append(Paragraph("Model 1: Fine-Tuned Resume Extraction Model (LLM)", h2_style))
    m1_box = [
        Paragraph("<b>• Base Architecture:</b> <code>unsloth/gpt-oss-20b-unsloth-bnb-4bit</code> or <code>Qwen2.5-7B</code>.", bullet_style),
        Paragraph("<b>• Fine-Tuning Technique:</b> <b>QLoRA</b> (Quantized Low-Rank Adaptation) in <b>4-bit NormalFloat (NF4)</b> with bfloat16 computation.", bullet_style),
        Paragraph("<b>• Adapter Checkpoint:</b> <code>JanCT05/resume-parser-gpt-oss-20b</code> (revision: <code>checkpoint-350-htmlclean</code>).", bullet_style),
        Paragraph("<b>• Training Dataset:</b> <code>sandeeppanem/resume-json-extraction-5k</code> (5,000 real-world resumes with verified JSON annotations).", bullet_style),
        Paragraph("<b>• Training Format:</b> <b>Harmony template</b> with reasoning effort disabled (<code>enable_thinking=false</code>) to output raw, valid JSON directly.", bullet_style),
        Paragraph("<b>• Output Schema Contract:</b> Exactly 15 structured fields: <i>current_title, previous_titles, current_company, previous_companies, years_experience, seniority, primary_domain, industries, core_skills, secondary_skills, tools, leadership_experience, key_achievements, location, summary</i>.", bullet_style),
        Paragraph("<b>• Why Contact Info is Separated:</b> Name, email, and phone are extracted via dedicated regex in <code>contact_extraction.py</code> to prevent LLM hallucinations on sensitive PII.", bullet_style),
    ]
    elements.append(make_box(m1_box, bg=BG_LIGHT, border=BORDER_COLOR))
    elements.append(Spacer(1, 10))

    # Model 2
    elements.append(Paragraph("Model 2: Dense Text Embedding Model", h2_style))
    m2_box = [
        Paragraph("<b>• Model Name:</b> <code>BAAI/bge-large-en-v1.5</code> (loaded via Python <code>sentence-transformers</code>).", bullet_style),
        Paragraph("<b>• Representation:</b> Produces dense <b>1,024-dimensional floating point vectors</b>.", bullet_style),
        Paragraph("<b>• Input Construction:</b> Formed strictly by concatenating 10 locked fields (title, previous titles, domain, industries, core skills, secondary skills, tools, experience, seniority, summary).", bullet_style),
        Paragraph("<b>• Academic Strength:</b> BGE is developed by the Beijing Academy of AI and consistently leads the Hugging Face MTEB (Massive Text Embedding Benchmark) for semantic search.", bullet_style),
    ]
    elements.append(make_box(m2_box, bg=BG_LIGHT, border=BORDER_COLOR))
    elements.append(Spacer(1, 10))

    # Model 3
    elements.append(Paragraph("Model 3: Vector Database (ChromaDB) & Similarity Matching", h2_style))
    m3_box = [
        Paragraph("<b>• Vector Engine:</b> <b>ChromaDB</b> with persistent local storage in <code>data/chroma</code>.", bullet_style),
        Paragraph("<b>• Indexing Algorithm:</b> <b>HNSW</b> (Hierarchical Navigable Small World graphs) for sub-millisecond nearest-neighbor search.", bullet_style),
        Paragraph("<b>• Distance Metric:</b> <b>Cosine Similarity</b>: <code>Cosine = (A · B) / (||A|| × ||B||)</code>.", bullet_style),
        Paragraph("<b>• Resilience Fallback:</b> If structured extraction fails on OCR-garbled text, the system falls back to embedding raw resume text so candidates are never lost.", bullet_style),
    ]
    elements.append(make_box(m3_box, bg=BG_LIGHT, border=BORDER_COLOR))
    elements.append(Spacer(1, 10))

    # Model 4
    elements.append(Paragraph("Model 4: Generative Reasoning & RAG LLM", h2_style))
    m4_box = [
        Paragraph("<b>• Live Provider:</b> <b>Groq Cloud API</b> running <code>llama-3.1-8b-instant</code> for ultra-low latency (<1s inference).", bullet_style),
        Paragraph("<b>• Alternative Provider:</b> <b>Anthropic Claude</b> (<code>claude-sonnet-5</code>).", bullet_style),
        Paragraph("<b>• Match Rationale Generation:</b> Combines candidate profile + job spec + similarity score into an evidence-based paragraph explaining the match.", bullet_style),
        Paragraph("<b>• Tailored Interview Questions:</b> Analyzes resume gaps against role tier to produce 4–5 rigorous questions with evaluation rubrics.", bullet_style),
        Paragraph("<b>• Mock Fallback:</b> Includes <code>MockLLMProvider</code> so the platform can run completely offline without API keys.", bullet_style),
    ]
    elements.append(make_box(m4_box, bg=BG_LIGHT, border=BORDER_COLOR))
    elements.append(Spacer(1, 14))

    # ==================== SECTION 4: COMPLETE TECH STACK ====================
    elements.append(PageBreak())
    elements.append(Paragraph("4. Complete Technology Stack & Architecture", h1_style))
    tech_table_data = [
        [Paragraph("Category", table_header_style), Paragraph("Technology", table_header_style), Paragraph("Role & Why We Used It", table_header_style)],
        [
            Paragraph("<b>Backend API</b>", table_cell_style),
            Paragraph("<b>FastAPI</b><br/>(Python 3.11+)", table_cell_style),
            Paragraph("Asynchronous, high-throughput web API with auto-generated Swagger docs and Pydantic validation.", table_cell_style)
        ],
        [
            Paragraph("<b>ASGI Server</b>", table_cell_style),
            Paragraph("<b>Uvicorn</b>", table_cell_style),
            Paragraph("Lightning-fast ASGI server for running asynchronous Python applications.", table_cell_style)
        ],
        [
            Paragraph("<b>Database ORM</b>", table_cell_style),
            Paragraph("<b>SQLAlchemy</b>", table_cell_style),
            Paragraph("Object Relational Mapper preventing SQL injection and abstracting database operations.", table_cell_style)
        ],
        [
            Paragraph("<b>Databases</b>", table_cell_style),
            Paragraph("<b>SQLite & PostgreSQL</b>", table_cell_style),
            Paragraph("SQLite for zero-config local demos; PostgreSQL for production multi-tenant deployments.", table_cell_style)
        ],
        [
            Paragraph("<b>Migrations</b>", table_cell_style),
            Paragraph("<b>Alembic</b>", table_cell_style),
            Paragraph("Version control for database schema migrations.", table_cell_style)
        ],
        [
            Paragraph("<b>Vector Storage</b>", table_cell_style),
            Paragraph("<b>ChromaDB</b>", table_cell_style),
            Paragraph("Embeddings database using HNSW indexing for rapid cosine similarity retrieval.", table_cell_style)
        ],
        [
            Paragraph("<b>Frontend UI</b>", table_cell_style),
            Paragraph("<b>React 18 & TypeScript</b>", table_cell_style),
            Paragraph("Component-driven reactive UI with compile-time type safety preventing runtime crashes.", table_cell_style)
        ],
        [
            Paragraph("<b>Build Tool</b>", table_cell_style),
            Paragraph("<b>Vite 8</b>", table_cell_style),
            Paragraph("Next-generation frontend bundler providing sub-second startup and Hot Module Replacement.", table_cell_style)
        ],
        [
            Paragraph("<b>Styling</b>", table_cell_style),
            Paragraph("<b>Tailwind CSS v4</b>", table_cell_style),
            Paragraph("Modern utility-first CSS framework for responsive layout and dark-mode styling.", table_cell_style)
        ],
        [
            Paragraph("<b>Auth & Security</b>", table_cell_style),
            Paragraph("<b>PyJWT & Passlib / Bcrypt</b>", table_cell_style),
            Paragraph("Bcrypt password hashing and stateless 60-minute JWT bearer token authorization.", table_cell_style)
        ],
        [
            Paragraph("<b>Containerization</b>", table_cell_style),
            Paragraph("<b>Docker & Docker Compose</b>", table_cell_style),
            Paragraph("Complete multi-container orchestration for backend, frontend, and DB with one command.", table_cell_style)
        ],
    ]
    t_tech = Table(tech_table_data, colWidths=[90, 110, 304])
    t_tech.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_tech)
    elements.append(Spacer(1, 14))

    # ==================== SECTION 5: 5-STAGE WORKFLOW ====================
    elements.append(Paragraph("5. The 5 End-to-End System Workflow Stages", h1_style))
    workflow_stages = [
        Paragraph("<b>Stage 1: Resume Ingestion & Parsing:</b> Upload PDF/Word → OCR fallback for scanned images → QLoRA LLM extracts 15 structured fields → Contact extractor extracts phone/email/links.", bullet_style),
        Paragraph("<b>Stage 2: Semantic RAG Matching:</b> 10 locked fields vectorized via BGE-large → ChromaDB calculates Cosine Similarity % → Groq/Claude writes evidence-backed match rationale.", bullet_style),
        Paragraph("<b>Stage 3: Tiered HITL Approvals:</b> Role-based approval routing: Junior/Mid → Hiring Manager; Senior → Director then VP; Exec → CEO. Full audit trail recorded.", bullet_style),
        Paragraph("<b>Stage 4: Interview Console & Scorecards:</b> AI generates tailored questions → Interviewers grade candidates on 1.0–5.0 rubrics → Dual Technical vs HR consensus calculated.", bullet_style),
        Paragraph("<b>Stage 5: Offer Letter & Onboarding Portal:</b> Automated markdown/PDF offer letters → Candidate electronic acceptance → Automated 6-step onboarding checklist (I-9, W-4, banking, laptop choice).", bullet_style),
    ]
    elements.append(make_box(workflow_stages, bg=BG_LIGHT, border=BORDER_COLOR))
    elements.append(Spacer(1, 14))

    # ==================== SECTION 6: TOP 10 VIVA QUESTIONS ====================
    elements.append(PageBreak())
    elements.append(Paragraph("6. Top 10 Viva / Presentation Questions with Model Answers", h1_style))
    elements.append(Paragraph(
        "Memorize these 10 model answers to handle questions from examiners or professors with ease:",
        body_style
    ))

    qa_pairs = [
        (
            "Q1: Why fine-tune an LLM instead of using regular ChatGPT or regex?",
            "Regex breaks when resumes have complex column layouts or custom wording. General ChatGPT can suffer from prompt drift or return unpredictable JSON formats. Fine-tuning with QLoRA on 5,000 resumes forces the model to guarantee a strict 15-key JSON schema every single time with zero formatting errors."
        ),
        (
            "Q2: What is QLoRA and why did you use it over full fine-tuning?",
            "Full fine-tuning updates all 20 billion weights, requiring expensive multi-GPU servers. QLoRA freezes the base model in 4-bit precision (NF4) and trains small low-rank adapter matrices. This reduces memory usage by over 75% while achieving near-identical accuracy."
        ),
        (
            "Q3: How does your semantic matching differ from keyword search?",
            "Keyword search fails if a candidate writes 'Container Orchestration' instead of 'Kubernetes'. Our BGE embedding model transforms text into 1,024-dimensional vectors that capture contextual meaning, and ChromaDB computes cosine similarity to identify conceptual matches."
        ),
        (
            "Q4: What is Human-In-The-Loop (HITL) and why is it needed?",
            "Fully automated hiring creates severe legal and ethical risks regarding AI bias. In ReSumo, AI is strictly an evaluator and assistant. Final hiring decisions require human approval through a multi-tiered hierarchy (Hiring Manager, Director, VP) based on role tier."
        ),
        (
            "Q5: How does the system handle scanned or image-based PDFs?",
            "The preprocessor inspects extracted text length. If a document has fewer than 10 words, it automatically triggers an OCR fallback on embedded images. If structured parsing fails, it embeds the raw text directly into ChromaDB so the candidate remains searchable."
        ),
        (
            "Q6: Why did you separate contact extraction from LLM extraction?",
            "LLMs can hallucinate personal names or transpose phone numbers. We use strict, deterministic regex and heuristic patterns for email, phone, and social links to guarantee 100% precision on sensitive contact details."
        ),
        (
            "Q7: How is multi-tenancy enforced in your application?",
            "Every database table (Jobs, Applications, Users, Onboarding) has a company_id foreign key. All FastAPI router queries enforce company-scoped filters, ensuring recruiters from Company A can never view or modify data from Company B."
        ),
        (
            "Q8: What vector distance metric did you choose and why?",
            "We chose Cosine Distance in ChromaDB. Cosine similarity measures the angle between vectors rather than their magnitude, making it ideal for comparing documents of varying lengths without biasing against shorter resumes."
        ),
        (
            "Q9: How does the Interviewer Rubric & Consensus work?",
            "Interviewers submit evaluations across specific dimensions (e.g. Technical Depth, System Design, Communication) on a 1.0 to 5.0 scale. The system computes average scores, separates Technical vs HR consensus, and provides a team consensus percentage."
        ),
        (
            "Q10: Can this system run completely offline without internet?",
            "Yes! The architecture includes MockLLMProvider and local SQLite/ChromaDB clients, allowing the entire application to be demoed completely offline without live external API keys."
        ),
    ]

    for q, a in qa_pairs:
        qa_box = [
            Paragraph(f"<b>{q}</b>", body_bold),
            Paragraph(f"<i>Answer:</i> {a}", body_style),
        ]
        elements.append(make_box(qa_box, bg=BG_LIGHT, border=BORDER_COLOR))
        elements.append(Spacer(1, 6))

    # ==================== SECTION 7: DEMO WALKTHROUGH ====================
    elements.append(PageBreak())
    elements.append(Paragraph("7. Live Demo Walkthrough (Screen-by-Screen Script)", h1_style))
    elements.append(Paragraph(
        "Follow this exact 5-step script if you need to demonstrate the live application running on your computer:",
        body_style
    ))

    demo_steps = [
        Paragraph("<b>Step 1: Login & Role Selection</b><br/>Go to <code>http://localhost:5173</code>. Click the 1-click <b>Recruiter</b> demo button. Explain that ReSumo features full Role-Based Access Control (Candidate, Recruiter, Approver, Interviewer, Admin).", bullet_style),
        Paragraph("<b>Step 2: Pipeline Kanban & Resume Ingestion</b><br/>Show the Recruitment Dashboard with candidate status columns (Uploaded, Parsed, Shortlisted, Pending Approval, Offered). Point out the extracted candidate profile cards.", bullet_style),
        Paragraph("<b>Step 3: Job Matching & RAG Rationale</b><br/>Navigate to <b>Jobs</b>. Click on a role to display the candidate rankings. Point out the <b>Match Score %</b> and read aloud the <b>AI Match Rationale</b> generated by the LLM.", bullet_style),
        Paragraph("<b>Step 4: Approver Hierarchy (HITL)</b><br/>Log out and log in as <b>Approver (manager@resumo.ai)</b>. Show the <b>Pending Approvals</b> queue. Show how high-level roles require multiple approval steps (Manager → Director → VP). Click <b>Approve</b> with a test note.", bullet_style),
        Paragraph("<b>Step 5: Candidate Portal & Onboarding</b><br/>Log in as a candidate. Show the formal <b>Offer Letter</b>. Click <b>Accept Offer</b>, and show how the <b>Post-Hire Onboarding Checklist</b> (I-9, W-4, banking, MacBook choice) automatically unlocks.", bullet_style),
    ]
    elements.append(make_box(demo_steps, bg=colors.HexColor("#EFF6FF"), border=ACCENT))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        "<b>Best of luck with your presentation tomorrow! You and your team are fully prepared.</b>",
        ParagraphStyle("WishGoodLuck", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=GREEN_ACCENT, alignment=1)
    ))

    # Build the document with two-pass canvas
    doc.build(elements, canvasmaker=NumberedCanvas)
    return output_filename


if __name__ == "__main__":
    out = "ReSumo_Project_Presentation_Guide.pdf"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    res = create_presentation_pdf(out)
    print(f"SUCCESS: Generated PDF at {os.path.abspath(res)}")
