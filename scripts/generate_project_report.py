from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "AI-BASED PLANT DISEASE DETECTION WEB APP.pdf"
TARGET_PAGES = 52
AUTHOR = "SHUAIB AHMED"
REGISTER_NO = "2313181033049"
GUIDE_PLACEHOLDER = "PROJECT GUIDE"


def clean_code_snippet(text: str, limit: int | None = None) -> str:
    text = text.replace("\t", "    ").replace("\ufeff", "")
    if limit and len(text) > limit:
        text = text[:limit].rstrip() + "\n# ... truncated for report ..."
    return text


def styles():
    sheet = getSampleStyleSheet()
    sheet.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=sheet["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=24,
            spaceAfter=12,
        )
    )
    sheet.add(
        ParagraphStyle(
            name="SubCenter",
            parent=sheet["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=16,
            spaceAfter=8,
        )
    )
    sheet.add(
        ParagraphStyle(
            name="BodyJustify",
            parent=sheet["BodyText"],
            alignment=TA_JUSTIFY,
            fontSize=10.5,
            leading=15,
            spaceAfter=8,
        )
    )
    sheet.add(
        ParagraphStyle(
            name="Section",
            parent=sheet["Heading1"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#1d4d2f"),
            spaceBefore=8,
            spaceAfter=10,
        )
    )
    sheet.add(
        ParagraphStyle(
            name="SubSection",
            parent=sheet["Heading2"],
            fontSize=11.5,
            leading=15,
            textColor=colors.HexColor("#1d4d2f"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    sheet.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=sheet["Code"],
            fontName="Courier",
            fontSize=7.6,
            leading=9.2,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=6,
        )
    )
    sheet.add(
        ParagraphStyle(
            name="Small",
            parent=sheet["Normal"],
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
        )
    )
    return sheet


def p(text: str, style_name: str, sheet) -> Paragraph:
    return Paragraph(text.strip().replace("\n", "<br/>"), sheet[style_name])


def add_bullets(story: list, items: list[str], sheet) -> None:
    for item in items:
        story.append(p(f"• {item}", "BodyJustify", sheet))


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(19.5 * cm, 1.4 * cm, str(doc.page))
    canvas.restoreState()


def add_placeholder_page(story: list, title: str, sheet) -> None:
    story.extend(
        [
            p(title, "Section", sheet),
            Spacer(1, 1.6 * cm),
            p("Insert your final screenshot or appendix content here.", "SubCenter", sheet),
            Spacer(1, 1.4 * cm),
            p("This page is intentionally reserved to match the sample report length and layout.", "SubCenter", sheet),
            PageBreak(),
        ]
    )


def build_story(extra_placeholder_pages: int = 0) -> list:
    sheet = styles()
    story: list = []

    app_py = clean_code_snippet((ROOT / "backend" / "App.py").read_text(encoding="utf-8"))
    cnn_py = clean_code_snippet((ROOT / "backend" / "CNN.py").read_text(encoding="utf-8"))
    app_tsx = clean_code_snippet((ROOT / "src" / "App.tsx").read_text(encoding="utf-8"))
    index_tsx = clean_code_snippet((ROOT / "src" / "pages" / "Index.tsx").read_text(encoding="utf-8"))
    login_tsx = clean_code_snippet((ROOT / "src" / "pages" / "Login.tsx").read_text(encoding="utf-8"))
    signup_tsx = clean_code_snippet((ROOT / "src" / "pages" / "Signup.tsx").read_text(encoding="utf-8"))
    dashboard_tsx = clean_code_snippet((ROOT / "src" / "pages" / "Dashboard.tsx").read_text(encoding="utf-8"))
    scan_tsx = clean_code_snippet((ROOT / "src" / "pages" / "Scan.tsx").read_text(encoding="utf-8"))
    results_tsx = clean_code_snippet((ROOT / "src" / "pages" / "Results.tsx").read_text(encoding="utf-8"))
    history_tsx = clean_code_snippet((ROOT / "src" / "pages" / "HistoryPage.tsx").read_text(encoding="utf-8"))
    auth_tsx = clean_code_snippet((ROOT / "src" / "contexts" / "AuthContext.tsx").read_text(encoding="utf-8"))
    protected_route_tsx = clean_code_snippet((ROOT / "src" / "components" / "ProtectedRoute.tsx").read_text(encoding="utf-8"))

    story.extend(
        [
            Spacer(1, 2 * cm),
            p("THE NEW COLLEGE", "TitleCenter", sheet),
            p(
                "(AN AUTONOMOUS INSTITUTION TO THE UNIVERSITY OF MADRAS)<br/>"
                "(ACCREDITED BY NAAC WITH 'A++' GRADE)",
                "SubCenter",
                sheet,
            ),
            Spacer(1, 0.8 * cm),
            p("Department of Computer Applications", "SubCenter", sheet),
            Spacer(1, 1.0 * cm),
            p("AI-BASED PLANT DISEASE DETECTION WEB APP", "TitleCenter", sheet),
            p(
                "A dissertation submitted in partial fulfillment of the requirements "
                "for the award of degree",
                "SubCenter",
                sheet,
            ),
            Spacer(1, 0.8 * cm),
            p("BACHELOR OF COMPUTER APPLICATIONS", "SubCenter", sheet),
            Spacer(1, 0.6 * cm),
            p("By", "SubCenter", sheet),
            p(AUTHOR, "SubCenter", sheet),
            p(f"REG. NO: {REGISTER_NO}", "SubCenter", sheet),
            p("Under the Guidance of", "SubCenter", sheet),
            p(GUIDE_PLACEHOLDER, "SubCenter", sheet),
            Spacer(1, 2.2 * cm),
            p("2025 - 2026", "SubCenter", sheet),
            PageBreak(),
            p("BONAFIDE CERTIFICATE", "TitleCenter", sheet),
            p(
                "This is to certify that the project work entitled <b>AI-BASED PLANT DISEASE "
                "DETECTION WEB APP</b> is a bonafide record of work carried out by "
                f"<b>{AUTHOR.title()}</b>, Reg. No: <b>{REGISTER_NO}</b> in partial fulfillment of the requirements for the award "
                "of the Degree of Bachelor of Computer Applications.",
                "BodyJustify",
                sheet,
            ),
            Spacer(1, 1.5 * cm),
            p("Project Guide", "SubCenter", sheet),
            Spacer(1, 0.8 * cm),
            p("Head of the Department", "SubCenter", sheet),
            PageBreak(),
            p("ACKNOWLEDGEMENT", "TitleCenter", sheet),
            p(
                "I express my sincere gratitude to all those who supported me in the successful "
                "completion of this project entitled <b>AI-BASED PLANT DISEASE DETECTION WEB APP</b>. "
                "I thank the management and faculty of the Department of Computer Applications for "
                "providing the academic environment and technical guidance needed for this work.",
                "BodyJustify",
                sheet,
            ),
            p(
                "I extend special thanks to my project guide for valuable suggestions, continuous "
                "encouragement, and timely support throughout the design, implementation, and testing "
                "stages of this application.",
                "BodyJustify",
                sheet,
            ),
            p(
                "I also thank my family and friends for their motivation and encouragement. Their support "
                "helped me complete this project with confidence and dedication.",
                "BodyJustify",
                sheet,
            ),
            PageBreak(),
            p("INDEX", "TitleCenter", sheet),
        ]
    )

    index_rows = [
        ["S. No.", "Title", "Page"],
        ["1", "Project Summary", "1"],
        ["2", "Abstract", "2"],
        ["3", "Chapter 1 - Introduction", "3"],
        ["4", "Chapter 2 - System Study", "6"],
        ["5", "Chapter 3 - System Design and Development", "9"],
        ["6", "Chapter 4 - Testing and Implementation", "14"],
        ["7", "Chapter 5 - Conclusion", "17"],
        ["8", "Bibliography", "19"],
        ["9", "Appendices", "20"],
    ]
    index_table = Table(index_rows, colWidths=[2 * cm, 11.5 * cm, 2.5 * cm])
    index_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe9df")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LEADING", (0, 0), (-1, -1), 13),
            ]
        )
    )
    story.extend([index_table, PageBreak()])

    story.extend(
        [
            p("PROJECT SUMMARY", "Section", sheet),
            p(
                "The <b>AI-Based Plant Disease Detection Web App</b> is a smart agriculture solution "
                "developed to help farmers, gardeners, and plant enthusiasts identify plant leaf diseases "
                "through image-based analysis. The system combines a modern React frontend with a Flask and "
                "PyTorch backend to deliver disease prediction results through a user-friendly web interface.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The application allows users to create an account, sign in securely using Supabase "
                "authentication, upload a plant leaf image or capture one using a device camera, and submit "
                "the image for prediction. The backend preprocesses the image to 224 x 224 pixels, runs it "
                "through a convolutional neural network, and returns one of 39 disease or healthy-class labels.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The project focuses on practical usability, fast response time, and modular integration between "
                "frontend and backend services. Features such as scan history, result visualization, protected "
                "routes, and responsive UI design improve the overall user experience. The system demonstrates "
                "how artificial intelligence can be applied to real-world agricultural challenges.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The proposed application is especially useful in educational and prototype smart-farming environments "
                "where a quick first-level diagnosis can support better plant-care decisions. By turning model inference "
                "into a browser-based workflow, the project reduces technical barriers and makes AI features easier to access "
                "for users who may not have prior experience with machine learning systems.",
                "BodyJustify",
                sheet,
            ),
            p("ABSTRACT", "Section", sheet),
            p(
                "Agriculture plays a vital role in the economy, and the early detection of plant diseases is "
                "essential for reducing crop loss and improving productivity. Traditional disease diagnosis often "
                "requires expert inspection, making it time-consuming and inaccessible in many field conditions. "
                "The proposed <b>AI-Based Plant Disease Detection Web App</b> addresses this problem through a web "
                "application that automates disease identification from plant leaf images.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The system uses a convolutional neural network trained for 39 plant disease categories, including "
                "healthy leaf classes. The frontend is built with React, TypeScript, Vite, Tailwind CSS, and "
                "component utilities, while the backend is developed using Flask, PyTorch, TorchVision, and PIL. "
                "Supabase is used for user authentication, enabling secure login and signup functionality.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The application supports image upload, drag-and-drop interaction, camera capture on compatible "
                "devices, protected dashboard views, and display of prediction results. By combining machine "
                "learning inference with an interactive web interface, the project provides an efficient, scalable, "
                "and easy-to-use solution for plant health monitoring.",
                "BodyJustify",
                sheet,
            ),
            p(
                "In addition to its technical implementation, the project highlights the broader importance of digital tools "
                "in agriculture. A system that can identify disease symptoms early can help reduce unnecessary pesticide use, "
                "improve crop management practices, and support timely intervention. For this reason, the application serves "
                "both as a software project and as a demonstration of AI-assisted agricultural support.",
                "BodyJustify",
                sheet,
            ),
            PageBreak(),
        ]
    )

    story.extend(
        [
            p("CHAPTER 1 - INTRODUCTION", "Section", sheet),
            p("1.1 Introduction to the Project", "SubSection", sheet),
            p(
                "Plant diseases reduce agricultural yield and quality, directly affecting food production and farmer "
                "income. In many cases, disease symptoms appear on leaf surfaces, making image-based analysis a useful "
                "approach for early diagnosis. This project introduces an AI-powered web application that identifies "
                "plant diseases from leaf images and presents the output through an accessible browser-based interface.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The system is designed to bridge the gap between deep learning models and end users. Instead of requiring "
                "specialist software, the application delivers prediction through a standard web flow: authentication, image "
                "selection, upload, analysis, and result display. This makes the solution suitable for educational use, small "
                "agriculture projects, and future field deployment scenarios.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The objective of the project is not only to display a predicted label, but also to demonstrate how an end-to-end "
                "software system can be built around an AI model. The user interacts with a polished interface, the backend handles "
                "preprocessing and prediction, and the final result is shown in a form that can be extended later with confidence "
                "scores, remedies, and disease explanations.",
                "BodyJustify",
                sheet,
            ),
            p("1.2 System Specification", "SubSection", sheet),
            p(
                "The project follows a web-based client-server architecture. The React frontend handles navigation, image "
                "selection, and result rendering, while the Flask backend performs model loading, preprocessing, and prediction. "
                "Supabase supports account-based access control for protected pages such as dashboard, scan, history, and profile.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The design supports maintainability because each layer has a clear responsibility. The frontend focuses on interaction "
                "and presentation, the backend focuses on AI inference, and the authentication service manages identity and sessions. "
                "This separation allows the application to be updated module by module without redesigning the entire system.",
                "BodyJustify",
                sheet,
            ),
            p("1.2.1 Hardware Configuration", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "Processor: Intel Core i3 or above",
            "RAM: Minimum 4 GB, 8 GB recommended",
            "Storage: At least 2 GB free for source code, dependencies, and trained model",
            "Camera: Optional mobile or laptop camera for direct image capture",
        ],
        sheet,
    )
    story.append(p("1.2.2 Software Specification", "SubSection", sheet))
    add_bullets(
        story,
        [
            "Frontend: React 18, TypeScript, Vite, Tailwind CSS, Radix UI, Framer Motion",
            "Backend: Flask, Flask-CORS, PyTorch, TorchVision, Pillow",
            "Authentication: Supabase",
            "Model Input Size: 224 x 224 RGB images",
            "Model Output: 39 disease or healthy categories",
            "Operating System: Windows, Linux, or macOS",
            "Browser: Chrome, Edge, or any modern browser",
        ],
        sheet,
    )
    story.append(PageBreak())

    story.extend(
        [
            p("CHAPTER 2 - SYSTEM STUDY", "Section", sheet),
            p("2.1 Existing System", "SubSection", sheet),
            p(
                "Conventional plant disease detection often depends on manual inspection by agricultural experts or laboratory "
                "testing. Such methods may be accurate but are not always available to users in remote or time-sensitive environments. "
                "In many cases, farmers rely on visual guesswork, which can result in delayed treatment or incorrect chemical usage.",
                "BodyJustify",
                sheet,
            ),
            p("2.2 Drawbacks of Existing System", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "Requires expert knowledge for reliable diagnosis",
            "Manual inspection can be slow and inconsistent",
            "Difficult to scale for many users or repeated monitoring",
            "Limited accessibility in remote locations",
            "Higher risk of crop damage due to delayed treatment",
        ],
        sheet,
    )
    story.extend(
        [
            p("2.3 Proposed System", "SubSection", sheet),
            p(
                "The proposed system is an AI-enabled web application that automates the disease detection process using leaf images. "
                "Users can upload an image or capture one from a device camera, and the backend model classifies the image into one "
                "of 39 predefined categories. The output is returned as a predicted disease label and displayed in a clean results page.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The system also includes user authentication, dashboard access, scan history scaffolding, and mobile-friendly UI flows. "
                "This creates a practical foundation for future enhancements such as confidence visualization, treatment recommendations, "
                "cloud storage, and live deployment for field use.",
                "BodyJustify",
                sheet,
            ),
            p(
                "Because the proposed system is web-based, it can be accessed using common devices such as laptops and smartphones without "
                "requiring dedicated software installation. This makes the solution more flexible and easier to distribute, especially in "
                "environments where users need a lightweight and accessible diagnostic tool.",
                "BodyJustify",
                sheet,
            ),
            p("2.4 Advantages of Proposed System", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "Fast disease detection through automated image classification",
            "Easy-to-use interface for both desktop and mobile users",
            "Reduced dependence on immediate expert availability",
            "Secure user access with Supabase authentication",
            "Modular architecture for future scaling and deployment",
        ],
        sheet,
    )
    story.append(PageBreak())

    story.extend(
        [
            p("CHAPTER 3 - SYSTEM DESIGN AND DEVELOPMENT", "Section", sheet),
            p("3.1 File Design", "SubSection", sheet),
            p(
                "The project is organized into two major parts: a frontend folder that contains the React application and a backend folder "
                "that contains the Flask API and trained PyTorch model. The frontend manages routing, pages, UI components, and authentication "
                "state. The backend contains the CNN architecture, model weights, image preprocessing pipeline, and prediction endpoint.",
                "BodyJustify",
                sheet,
            ),
            p(
                "This file organization improves maintainability because developers can work independently on presentation logic and AI services. "
                "Reusable components, page-level modules, and context-based state management on the frontend reduce duplication, while the backend "
                "keeps model-specific logic isolated from the browser layer.",
                "BodyJustify",
                sheet,
            ),
            p("3.2 Input Design", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "User email and password for login/signup",
            "Plant image upload through file picker",
            "Drag-and-drop image submission",
            "Camera capture input on supported devices",
        ],
        sheet,
    )
    story.extend(
        [
            p("3.3 Output Design", "SubSection", sheet),
            p(
                "The output screen displays the scanned image and the predicted disease name. The dashboard presents high-level user activity "
                "metrics such as total scans, diseases detected, and healthy plants based on locally stored history data. UI elements are "
                "designed to be visually clear, animated, and responsive across screen sizes.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The output design is intentionally simple so that the result can be understood quickly. Visual separation between image preview, "
                "analysis state, and final prediction helps the user follow the scan flow clearly. This reduces confusion during use and supports "
                "a better experience for first-time users.",
                "BodyJustify",
                sheet,
            ),
            p("3.4 System Architecture", "SubSection", sheet),
        ]
    )

    architecture_rows = [
        ["Layer", "Responsibility"],
        ["React Frontend", "Routing, forms, dashboard, scan workflow, results rendering"],
        ["Supabase Auth", "Signup, login, session management, protected routes"],
        ["Flask API", "Receives image, preprocesses input, runs inference, returns JSON"],
        ["CNN Model", "Classifies plant leaf image into 39 categories"],
    ]
    arch_table = Table(architecture_rows, colWidths=[4.5 * cm, 12 * cm])
    arch_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe9df")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("LEADING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story.extend([arch_table, Spacer(1, 0.2 * cm)])

    story.extend(
        [
            p("3.5 System Development", "SubSection", sheet),
            p(
                "The frontend was developed using component-based React pages such as landing, login, signup, dashboard, scan, results, "
                "history, and profile. The backend was implemented in Flask with CORS support to allow requests from the frontend. The "
                "model file is loaded once at server start-up to reduce prediction latency during user requests.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The development process emphasized modularity and ease of testing. Individual UI pages were verified in isolation before "
                "integration with authentication and backend communication. This step-by-step implementation helped ensure that routing, "
                "API requests, and result rendering behaved consistently throughout the application.",
                "BodyJustify",
                sheet,
            ),
            p("3.5.1 Description of Modules", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "Authentication Module: Handles user signup, login, logout, and session restoration through Supabase.",
            "Dashboard Module: Displays summary cards and navigation shortcuts for main user actions.",
            "Scan Module: Accepts image input, validates file type, previews images, and sends POST requests to the backend.",
            "Prediction Module: Applies resize and tensor transformation, loads the CNN model, and returns the predicted class label.",
            "Results Module: Displays scanned image and diagnosis result after successful prediction.",
            "History Module: Stores and reads previous scans from browser local storage for quick review.",
        ],
        sheet,
    )
    story.append(PageBreak())

    story.extend(
        [
            p("CHAPTER 4 - TESTING AND IMPLEMENTATION", "Section", sheet),
            p("4.1 System Testing", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "Authentication testing for signup, login, logout, and route protection",
            "Input validation testing for accepted image file types",
            "API testing for POST /predict requests with image payloads",
            "Prediction testing to verify model response format and class label output",
            "UI testing for scan flow, result navigation, and error handling",
            "Responsive testing for desktop and mobile layouts",
        ],
        sheet,
    )
    story.extend(
        [
            p("4.2 Implementation", "SubSection", sheet),
            p(
                "The application is implemented as a locally runnable full-stack project. The frontend runs through the Vite development "
                "server and communicates with the Flask backend at <b>http://127.0.0.1:5001/predict</b>. The backend loads the "
                "<b>plant_disease_model_1_latest.pt</b> file and performs inference on CPU. User authentication is enabled through "
                "Supabase using the configured project URL and anonymous key.",
                "BodyJustify",
                sheet,
            ),
            p(
                "This development setup supports quick iteration and demonstrates practical integration between machine learning inference, "
                "web UI workflows, and account-based access control. The same architecture can later be adapted for cloud hosting and API-based deployment.",
                "BodyJustify",
                sheet,
            ),
            p(
                "Implementation also includes cross-origin communication between the frontend and backend, image preprocessing using TorchVision transforms, "
                "and a structured response flow where the JSON output from Flask is passed into the React results page. These steps show how separate technologies "
                "can be combined into a single functioning AI application.",
                "BodyJustify",
                sheet,
            ),
            PageBreak(),
            p("CHAPTER 5 - CONCLUSION", "Section", sheet),
            p(
                "The <b>AI-Based Plant Disease Detection Web App</b> successfully demonstrates how artificial intelligence can be integrated "
                "with a modern web stack to solve an important real-world problem in agriculture. The system offers an accessible platform "
                "for leaf-based disease diagnosis by combining a trained convolutional neural network with a clean React user interface and "
                "a Flask prediction API.",
                "BodyJustify",
                sheet,
            ),
            p(
                "The project shows strength in modular design, secure authentication, responsive scanning workflows, and practical machine "
                "learning deployment. It can support students, hobby growers, and future agricultural use cases, while also serving as a "
                "strong academic demonstration of applied AI in web development.",
                "BodyJustify",
                sheet,
            ),
            p(
                "From an academic perspective, the project demonstrates the integration of concepts from artificial intelligence, image processing, web development, "
                "user authentication, and API-based communication. From a practical perspective, it shows how technology can be used to create accessible support tools "
                "for agriculture and plant care.",
                "BodyJustify",
                sheet,
            ),
            p("5.1 Future Enhancements", "SubSection", sheet),
        ]
    )
    add_bullets(
        story,
        [
            "Display confidence score and top-k predictions from the CNN model",
            "Add treatment suggestions and prevention guidance based on disease label",
            "Store scan history in a cloud database instead of local storage only",
            "Deploy the backend model to a scalable cloud environment",
            "Add multilingual support for wider accessibility",
            "Integrate camera-based real-time scanning and offline caching",
        ],
        sheet,
    )
    story.extend(
        [
            p("BIBLIOGRAPHY", "Section", sheet),
            p("1. Flask Documentation - https://flask.palletsprojects.com/", "BodyJustify", sheet),
            p("2. PyTorch Documentation - https://pytorch.org/docs/", "BodyJustify", sheet),
            p("3. React Documentation - https://react.dev/", "BodyJustify", sheet),
            p("4. Vite Documentation - https://vite.dev/", "BodyJustify", sheet),
            p("5. Supabase Documentation - https://supabase.com/docs", "BodyJustify", sheet),
            PageBreak(),
            p("APPENDICES", "Section", sheet),
            p("A. Backend API Code Snippet (App.py)", "SubSection", sheet),
            Preformatted(app_py, sheet["CodeBlock"]),
            p("B. CNN Architecture Snippet (CNN.py)", "SubSection", sheet),
            Preformatted(cnn_py, sheet["CodeBlock"]),
            PageBreak(),
            p("C. Application Routing Snippet (App.tsx)", "SubSection", sheet),
            Preformatted(app_tsx, sheet["CodeBlock"]),
            p("D. Landing Page Snippet (Index.tsx)", "SubSection", sheet),
            Preformatted(index_tsx, sheet["CodeBlock"]),
            PageBreak(),
            p("E. Login Page Snippet (Login.tsx)", "SubSection", sheet),
            Preformatted(login_tsx, sheet["CodeBlock"]),
            p("F. Signup Page Snippet (Signup.tsx)", "SubSection", sheet),
            Preformatted(signup_tsx, sheet["CodeBlock"]),
            PageBreak(),
            p("G. Dashboard Page Snippet (Dashboard.tsx)", "SubSection", sheet),
            Preformatted(dashboard_tsx, sheet["CodeBlock"]),
            p("C. Scan Page Snippet (Scan.tsx)", "SubSection", sheet),
            Preformatted(scan_tsx, sheet["CodeBlock"]),
            PageBreak(),
            p("H. Results Page Snippet (Results.tsx)", "SubSection", sheet),
            Preformatted(results_tsx, sheet["CodeBlock"]),
            PageBreak(),
            p("I. History Page Snippet (HistoryPage.tsx)", "SubSection", sheet),
            Preformatted(history_tsx, sheet["CodeBlock"]),
            p("J. Authentication Context Snippet (AuthContext.tsx)", "SubSection", sheet),
            Preformatted(auth_tsx, sheet["CodeBlock"]),
            PageBreak(),
            p("K. Protected Route Snippet (ProtectedRoute.tsx)", "SubSection", sheet),
            Preformatted(protected_route_tsx, sheet["CodeBlock"]),
            p(
                "Note: This report was generated from the current project workspace and mirrors the structure of the sample academic PDF while "
                "using the implementation details of the LeafSense AI project.",
                "Small",
                sheet,
            ),
        ]
    )

    for title in [
        "SCREENSHOTS - LANDING PAGE",
        "SCREENSHOTS - LOGIN PAGE",
        "SCREENSHOTS - DASHBOARD PAGE",
        "SCREENSHOTS - SCAN PAGE",
        "SCREENSHOTS - RESULTS PAGE",
        "SCREENSHOTS - HISTORY PAGE",
    ]:
        add_placeholder_page(story, title, sheet)

    for index in range(extra_placeholder_pages):
        add_placeholder_page(story, f"APPENDIX PLACEHOLDER PAGE {index + 1}", sheet)

    if story and isinstance(story[-1], PageBreak):
        story.pop()

    return story


def build_pdf(extra_placeholder_pages: int) -> int:
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
        title="AI-BASED PLANT DISEASE DETECTION WEB APP",
        author=AUTHOR.title(),
    )
    doc.build(build_story(extra_placeholder_pages), onFirstPage=page_number, onLaterPages=page_number)
    return len(PdfReader(str(OUTPUT)).pages)


def main() -> None:
    extra = 0
    pages = build_pdf(extra)
    while pages < TARGET_PAGES:
        extra += TARGET_PAGES - pages
        pages = build_pdf(extra)
    print(OUTPUT)
    print(f"pages={pages}")


if __name__ == "__main__":
    main()
