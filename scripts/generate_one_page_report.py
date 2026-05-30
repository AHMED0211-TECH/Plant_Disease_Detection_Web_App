from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "AI-BASED PLANT DISEASE DETECTION WEB APP.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 56
RIGHT = 56
TOP = PAGE_HEIGHT - 56
BOTTOM = 56
TEXT_WIDTH = PAGE_WIDTH - LEFT - RIGHT


def read_text(path: Path, max_lines: int = 68) -> str:
    lines = path.read_text(encoding="utf-8").replace("\t", "    ").splitlines()
    return "\n".join(lines[:max_lines])


def draw_page_number(c: canvas.Canvas, page_no: int) -> None:
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_WIDTH - 50, 30, str(page_no))


def draw_title_page(c: canvas.Canvas, title: str, page_no: int) -> None:
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 20, title)
    draw_page_number(c, page_no)
    c.showPage()


def draw_text_page(c: canvas.Canvas, title: str, paragraphs: list[str], bullets: list[str], page_no: int) -> None:
    y = TOP
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, y, title)
    y -= 28

    c.setFont("Helvetica", 10.5)
    blocks: list[tuple[str, list[str]]] = []
    total_lines = 0
    for para in paragraphs:
        lines = simpleSplit(para, "Helvetica", 10.5, TEXT_WIDTH)
        blocks.append(("para", lines))
        total_lines += len(lines)
    for bullet in bullets:
        lines = simpleSplit(f"- {bullet}", "Helvetica", 10.5, TEXT_WIDTH)
        blocks.append(("bullet", lines))
        total_lines += len(lines)

    usable_height = y - BOTTOM - 20
    base_line_gap = 14
    block_gap_count = max(len(blocks) - 1, 1)
    base_height = total_lines * base_line_gap + block_gap_count * 8
    extra_space = max(0, usable_height - base_height)
    extra_line_gap = min(4, extra_space / max(total_lines, 1))
    extra_block_gap = min(18, extra_space / block_gap_count) if block_gap_count else 0

    for index, (kind, lines) in enumerate(blocks):
        for line in lines:
            c.drawString(LEFT, y, line)
            y -= base_line_gap + extra_line_gap
        if index != len(blocks) - 1:
            y -= 8 + extra_block_gap

    draw_page_number(c, page_no)
    c.showPage()


def draw_code_page(c: canvas.Canvas, title: str, code: str, page_no: int) -> None:
    y = TOP
    c.setFont("Helvetica-Bold", 14)
    c.drawString(LEFT, y, title)
    y -= 24

    raw_lines = code.splitlines()
    usable_height = y - BOTTOM - 20
    line_gap = max(8.5, min(12.5, usable_height / max(len(raw_lines), 1)))

    c.setFont("Courier", 7.8)
    for raw_line in raw_lines:
        line = raw_line[:118]
        c.drawString(LEFT, y, line)
        y -= line_gap
        if y < BOTTOM + 10:
            break

    draw_page_number(c, page_no)
    c.showPage()


def draw_placeholder_page(c: canvas.Canvas, title: str, page_no: int) -> None:
    c.setFont("Helvetica-Bold", 16)
    c.drawString(LEFT, TOP, title)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 10, "Insert your screenshot here")
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 15, "This page is reserved so each content stays on a separate page.")
    draw_page_number(c, page_no)
    c.showPage()


def build_pages():
    return [
        ("text", "PROJECT SUMMARY", {
            "paragraphs": [
                "The AI-Based Plant Disease Detection Web App is a smart agriculture application developed to identify plant diseases from leaf images using deep learning. The main objective of the project is to provide a fast, simple, and accessible method for recognizing disease symptoms through a web browser.",
                "The system combines a React and TypeScript frontend with a Flask and PyTorch backend. Users can upload a plant leaf image or capture one from a camera-enabled device, and the backend processes the image to return a predicted disease class. The project supports secure user access, image preview, responsive design, and smooth navigation between scan and result views.",
                "This application demonstrates the practical use of artificial intelligence in agriculture. It reduces the dependency on manual visual inspection, supports early awareness of leaf health conditions, and creates a strong foundation for future features such as remedy recommendations, confidence scores, and cloud-based record keeping.",
                "A major strength of the project is the way it connects machine learning with a usable web interface. Instead of limiting the model to a notebook or standalone script, the system presents the prediction workflow in a form that can be used by students, developers, and future agriculture-focused users. The project therefore represents both a software engineering exercise and a meaningful applied AI solution.",
                "The application is also designed with extensibility in mind. Since the prediction engine, authentication flow, and interface pages are separated into modules, future developers can expand the project to include treatment suggestions, downloadable reports, cloud-backed scan history, or support for additional crops and disease classes without redesigning the full system."
            ],
            "bullets": []
        }),
        ("text", "ABSTRACT", {
            "paragraphs": [
                "Plant diseases affect crop yield, quality, and overall agricultural productivity. In many real-world situations, disease diagnosis depends on manual inspection by experts, which may be slow, inconsistent, or inaccessible. The AI-Based Plant Disease Detection Web App addresses this issue by providing a browser-based system that predicts plant diseases from leaf images.",
                "The application uses a convolutional neural network model trained for 39 plant disease and healthy classes. The frontend is built using React, TypeScript, Vite, Tailwind CSS, and supporting UI libraries, while the backend is implemented with Flask, PyTorch, TorchVision, and Pillow. Supabase authentication is integrated to manage secure access to user-facing features such as dashboard and scan history.",
                "The overall system demonstrates how AI, image processing, and web development can be combined into a practical agriculture-oriented software project. It offers speed, usability, modularity, and scope for enhancement, making it suitable for academic demonstration and future real-world deployment.",
                "From a technical perspective, the project highlights model inference flow, image preprocessing, API-based communication, authentication handling, and responsive page design within a single application. From a practical perspective, it shows how digital tools can support early plant disease awareness and encourage the adoption of intelligent systems in agriculture.",
                "The proposed solution is particularly relevant in settings where immediate expert consultation may not always be available. By offering a clear browser-based workflow for disease prediction, the system demonstrates how artificial intelligence can be transformed from a research concept into a practical user-focused service."
            ],
            "bullets": []
        }),
        ("title", "CHAPTER - 1", {}),
        ("text", "1.1 INTRODUCTION", {
            "paragraphs": [
                "Plant health monitoring is one of the important factors in agriculture because diseases can spread quickly and reduce productivity if not detected early. Leaves often carry visible symptoms such as spots, discoloration, fungal growth, curling, or dryness, making image-based disease analysis a useful approach for early diagnosis.",
                "The AI-Based Plant Disease Detection Web App is developed to make this process easier by allowing users to upload a leaf image and receive a disease prediction from a trained deep learning model. Instead of requiring technical knowledge of machine learning tools, the application wraps the prediction process inside a simple web workflow that is easy to operate.",
                "This project also demonstrates full-stack software integration. The frontend handles interaction and presentation, the backend handles model inference, and the authentication layer manages user access. Together, these parts form a complete AI-enabled application.",
                "The relevance of the project lies not only in disease prediction but also in the methodology used to develop it. The work shows how practical software engineering, machine learning deployment, and user-centered design can be combined to solve a real-world agricultural problem in a structured and academic manner."
            ],
            "bullets": []
        }),
        ("text", "1.2 SYSTEM SPECIFICATION", {
            "paragraphs": [
                "The project follows a client-server architecture. The client side is a React application that manages routing, forms, image preview, and result display. The server side is a Flask application that loads the trained model, preprocesses the image input, performs inference, and returns the predicted class in JSON format.",
                "The system is designed for easy maintainability by separating UI logic, authentication logic, and AI inference logic. Supabase is used for user account and session handling, while the Flask backend is responsible only for model-based prediction.",
                "Because the system is web-based, it can run through common browsers on laptops and mobile devices. This makes the application flexible, portable, and suitable for future deployment extensions.",
                "The architecture also supports future improvements in a practical manner. The frontend can be extended with better analytics and interface features, while the backend can be improved with optimized models or deployment changes without affecting the overall design pattern."
            ],
            "bullets": []
        }),
        ("text", "1.2.1 HARDWARE CONFIGURATION", {
            "paragraphs": [
                "The hardware requirements of the project are moderate because the application is built mainly for development and browser-based usage. Since the trained model is loaded on the backend, the client device is not responsible for AI computation."
            ],
            "bullets": [
                "Processor: Intel Core i3 or above",
                "RAM: Minimum 4 GB, 8 GB recommended",
                "Storage: 2 GB free space or more",
                "Display: Standard desktop or mobile screen",
                "Input Devices: Keyboard, mouse, and optional camera"
            ]
        }),
        ("text", "1.2.2 SOFTWARE SPECIFICATION", {
            "paragraphs": [
                "The software stack is selected to support both modern web interaction and deep learning inference. Each tool is used for a specific purpose in the system architecture."
            ],
            "bullets": [
                "Frontend: React, TypeScript, Vite, Tailwind CSS",
                "Backend: Python, Flask, Flask-CORS",
                "Deep Learning: PyTorch and TorchVision",
                "Image Handling: Pillow",
                "Authentication: Supabase",
                "Browser: Chrome, Edge, or equivalent modern browser",
                "Execution Environment: Localhost development setup"
            ]
        }),
        ("title", "CHAPTER - 2", {}),
        ("text", "2.1 EXISTING SYSTEM", {
            "paragraphs": [
                "Traditional plant disease identification is often done manually by farmers, agronomists, or crop experts. This method depends heavily on experience, and results can vary depending on the observer's knowledge and the clarity of visible symptoms.",
                "In many practical situations, access to experts is limited, especially when quick action is required. Laboratory testing may provide better accuracy, but it can be costly and time-consuming. As a result, there is a strong need for digital tools that can offer an initial diagnosis rapidly and conveniently.",
                "The existing system therefore lacks both speed and scalability. It is difficult to use repeatedly across many plants or in large areas of cultivation, and it does not automatically preserve diagnosis history in a digital, searchable format."
            ],
            "bullets": []
        }),
        ("text", "2.2 DRAWBACKS OF EXISTING SYSTEM", {
            "paragraphs": [
                "The existing manual approach to disease detection has several weaknesses that make it unsuitable for fast and repeatable diagnosis in many day-to-day situations."
            ],
            "bullets": [
                "High dependency on expert knowledge",
                "Slow diagnosis process in urgent crop conditions",
                "Risk of human error and inconsistent judgment",
                "Limited digital record keeping",
                "Reduced accessibility for remote users"
            ]
        }),
        ("text", "2.3 PROPOSED SYSTEM", {
            "paragraphs": [
                "The proposed system is an AI-powered web application that predicts plant diseases from uploaded leaf images. The user interacts with a simple scan page, submits an image, and receives a disease class from the backend model.",
                "The application improves accessibility because it uses standard web technologies and does not require direct interaction with machine learning code. It also supports account-based access, result display, and a structure for storing previous scan information.",
                "This approach creates a more practical and scalable solution than manual-only diagnosis methods.",
                "By moving the model behind an easy-to-use interface, the proposed system makes disease detection available in a form that can be adapted for farms, educational demonstrations, agriculture startups, and future smart-crop platforms."
            ],
            "bullets": []
        }),
        ("text", "2.4 ADVANTAGES OF PROPOSED SYSTEM", {
            "paragraphs": [
                "The AI-Based Plant Disease Detection Web App provides several practical advantages over traditional diagnosis workflows."
            ],
            "bullets": [
                "Fast disease prediction through deep learning",
                "Simple interface for non-technical users",
                "Responsive web access on different devices",
                "Secure account-based feature access",
                "Expandable architecture for future enhancements"
            ]
        }),
        ("title", "CHAPTER - 3", {}),
        ("text", "3. SYSTEM DESIGN AND DEVELOPMENT", {
            "paragraphs": [
                "The system design and development phase transforms the project idea into a structured software solution. The design follows clear separation between interface handling, authentication, and prediction logic so that each part of the system can be updated independently.",
                "The frontend is organized into pages, context providers, hooks, and reusable UI components. The backend contains the CNN architecture, model weights, preprocessing steps, and the prediction route. This modular design improves readability, maintainability, and integration.",
                "The development approach gives equal importance to both functionality and usability. The system is not built only to run predictions, but also to guide the user through login, upload, analysis, and result interpretation in a way that feels consistent and organized."
            ],
            "bullets": []
        }),
        ("text", "3.1 FILE DESIGN", {
            "paragraphs": [
                "The project directory is divided into frontend and backend sections. The frontend contains routes such as landing page, login, signup, dashboard, scan, results, history, and profile pages. The backend contains App.py, CNN.py, the trained model file, and environment support.",
                "This design ensures that frontend changes do not directly disturb backend inference logic. It also makes debugging easier because files are grouped by responsibility.",
                "The file design also helps future maintenance because reusable code is placed in shared components and context modules. This reduces duplication and allows each functional part of the application to be understood more clearly."
            ],
            "bullets": []
        }),
        ("text", "3.2 INPUT DESIGN", {
            "paragraphs": [
                "The input design focuses on collecting valid user information and valid plant images. Authentication inputs include email and password, while scan inputs include image files selected through upload, drag-and-drop, or camera capture.",
                "Validation is important because unsupported inputs can break the prediction flow. For this reason, the interface checks for image file types and shows the selected image before analysis.",
                "The input design is intentionally simple so that users can understand the scan process immediately. A minimal number of steps helps reduce confusion and supports faster interaction during repeated use."
            ],
            "bullets": []
        }),
        ("text", "3.3 OUTPUT DESIGN", {
            "paragraphs": [
                "The output design is simple and centered on usability. After prediction, the result page displays the scanned image and the predicted disease name. The dashboard uses summary cards to show overall scan activity and quick access to main actions.",
                "Animations, spacing, and clear labels improve the readability of the interface and help the user understand the analysis process.",
                "The presentation style is designed to reduce ambiguity. By clearly separating the image area, loading state, and final result, the user can follow the sequence of operations and better trust the output generated by the system."
            ],
            "bullets": []
        }),
        ("text", "3.4 DATABASE DESIGN", {
            "paragraphs": [
                "The current implementation uses Supabase authentication for user identity management and browser local storage for lightweight scan history support. This design is enough for the prototype stage and demonstrates how persistent state can be handled across sessions.",
                "The approach can be extended later by storing complete scan results in a cloud database, enabling account-specific records, analytics, and synchronization.",
                "Although the present system is lightweight, it still demonstrates important concepts of state persistence and user-specific interaction. These concepts form a useful starting point for future large-scale data handling."
            ],
            "bullets": []
        }),
        ("text", "3.4.1 AUTHENTICATION DESIGN", {
            "paragraphs": [
                "Authentication is handled through Supabase and is integrated into the frontend using a shared context provider. When the application loads, it checks for an existing user session and updates the authentication state accordingly.",
                "Protected routes ensure that only authenticated users can access internal pages such as dashboard, scan, results, history, and profile. This improves security and creates a more structured application flow for account-based features."
            ],
            "bullets": [
                "Session retrieval on application load",
                "Login and signup through Supabase auth methods",
                "Logout for secure session termination",
                "ProtectedRoute wrapper for restricted pages"
            ]
        }),
        ("text", "3.5 SYSTEM DEVELOPMENT", {
            "paragraphs": [
                "The development process followed a modular and iterative approach. Core pages and routes were created first, then authentication was integrated, followed by image upload behavior, backend connectivity, and prediction handling.",
                "Each module was tested after implementation so that navigation, API communication, and result rendering worked reliably before the next feature was added.",
                "This development approach made it easier to identify problems early and improve the application in manageable steps. It also ensured that design decisions could be refined gradually instead of being fixed too early in the project."
            ],
            "bullets": []
        }),
        ("text", "3.5.1 DESCRIPTION OF MODULES", {
            "paragraphs": [
                "The application is divided into functional modules to make development and maintenance easier."
            ],
            "bullets": [
                "Landing Module: Introduces the project and navigation entry points",
                "Authentication Module: Handles login, signup, logout, and sessions",
                "Dashboard Module: Shows user summary cards and shortcuts",
                "Scan Module: Accepts image input and sends it to the backend",
                "Prediction Module: Preprocesses images and returns class labels",
                "Results Module: Displays scan output clearly",
                "History Module: Stores and retrieves previous scan information"
            ]
        }),
        ("title", "CHAPTER - 4", {}),
        ("text", "4. TESTING AND IMPLEMENTATION", {
            "paragraphs": [
                "Testing is essential for verifying that each component of the application functions correctly. Since the project combines frontend logic, user authentication, file handling, and backend AI inference, integration testing is particularly important.",
                "The implementation stage focuses on running the project in a local full-stack environment and ensuring smooth communication between Vite, Flask, Supabase, and the trained CNN model.",
                "This phase confirms that the software is not only theoretically designed but also practically executable. The stability of interactions between modules is important because the user experience depends on the coordinated behavior of all integrated technologies."
            ],
            "bullets": []
        }),
        ("text", "4.0.1 MODEL WORKFLOW", {
            "paragraphs": [
                "The prediction workflow begins when the user selects an image in the scan page. The image file is packed into form-data and sent to the Flask backend through a POST request. The backend opens the image, converts it to RGB format, resizes it to 224 x 224, and transforms it into a tensor.",
                "After preprocessing, the tensor is passed through the trained CNN model. The model outputs prediction scores across 39 classes, and the class with the highest score is selected as the final result. This result is then returned to the frontend and displayed to the user.",
                "The workflow is designed to be direct and efficient. By keeping the prediction route focused on a single task, the system minimizes unnecessary processing and simplifies both debugging and future optimization."
            ],
            "bullets": [
                "Image upload",
                "Form-data submission",
                "Image preprocessing",
                "CNN inference",
                "Class mapping and result response"
            ]
        }),
        ("text", "4.1 SYSTEM TESTING", {
            "paragraphs": [
                "Different test scenarios were considered to confirm that the application behaves as expected under normal usage."
            ],
            "bullets": [
                "Authentication testing for signup, login, and logout",
                "Protected route testing for dashboard and scan pages",
                "Image input testing for supported file formats",
                "Prediction endpoint testing using form-data uploads",
                "Result navigation testing after successful inference",
                "Responsive UI testing on desktop and mobile screens"
            ]
        }),
        ("text", "4.2 IMPLEMENTATION", {
            "paragraphs": [
                "The frontend runs through the Vite development server, while the backend runs through Flask on port 5001. The trained model file is loaded on the backend and used to produce predictions for incoming images.",
                "Supabase manages authentication and session state, allowing account-based navigation to protected pages. This implementation demonstrates the practical combination of AI inference, browser UI, and authentication services within one project.",
                "The architecture can later be adapted for cloud hosting, database storage, and production deployment.",
                "The implementation therefore serves as a realistic prototype rather than a purely theoretical model demonstration. It shows how the system components interact in a usable environment and provides a clear foundation for future enhancement and deployment."
            ],
            "bullets": []
        }),
        ("text", "4.2.1 LIMITATIONS OF CURRENT IMPLEMENTATION", {
            "paragraphs": [
                "The current version of the system is a functional prototype, but it still has several limitations. At present, the result page mainly shows the predicted disease name and does not yet provide confidence scoring, remedy suggestions, or full database-backed storage of scan records.",
                "The backend is configured for local execution and CPU inference, which is practical for development but may not be optimal for larger deployment scenarios. These limitations do not reduce the academic value of the project, but they do identify areas for future engineering improvement."
            ],
            "bullets": [
                "No online deployment in the current version",
                "No confidence score shown in the UI",
                "History data stored locally instead of cloud database",
                "Inference currently runs on local CPU"
            ]
        }),
        ("title", "CHAPTER - 5", {}),
        ("text", "CONCLUSION", {
            "paragraphs": [
                "The AI-Based Plant Disease Detection Web App successfully demonstrates how artificial intelligence can be used in a practical and accessible agricultural application. By combining a trained CNN model with a modern full-stack web interface, the project creates a useful system for plant leaf disease prediction.",
                "The project also shows the integration of important computing concepts such as image preprocessing, authentication, API communication, route protection, responsive design, and modular development. These qualities make it both a meaningful academic project and a valuable base for future real-world improvement.",
                "Overall, the application highlights the usefulness of AI-assisted diagnosis tools in supporting better awareness of plant health conditions.",
                "The final outcome of the project is not only a working prediction application, but also a structured demonstration of how interdisciplinary technologies can be combined to solve a practical problem. For this reason, the project stands as both a technical achievement and a relevant academic contribution."
            ],
            "bullets": []
        }),
        ("text", "5.0.1 SOCIAL AND PRACTICAL IMPACT", {
            "paragraphs": [
                "A system like this can be useful in educational institutions, small farms, gardening communities, and agricultural startups where an immediate first-level diagnosis is valuable. Even when it does not replace expert consultation, it can still help users identify likely disease categories more quickly.",
                "In practical terms, early disease awareness may support better plant-care decisions, reduce crop loss, and encourage wider adoption of digital tools in agriculture. This project therefore has both technical and social relevance."
            ],
            "bullets": []
        }),
        ("text", "5.1 FUTURE ENHANCEMENTS", {
            "paragraphs": [
                "The present system can be extended further to improve usability, accuracy presentation, and practical deployment."
            ],
            "bullets": [
                "Add confidence scores and top prediction alternatives",
                "Include treatment and prevention recommendations",
                "Store complete scan history in cloud storage",
                "Deploy the application online for public access",
                "Support multilingual interfaces",
                "Increase the number of supported crops and diseases"
            ]
        }),
        ("text", "BIBLIOGRAPHY", {
            "paragraphs": [
                "The following references were used for implementation guidance and technical understanding."
            ],
            "bullets": [
                "Flask Documentation - https://flask.palletsprojects.com/",
                "PyTorch Documentation - https://pytorch.org/docs/",
                "React Documentation - https://react.dev/",
                "Vite Documentation - https://vite.dev/",
                "Supabase Documentation - https://supabase.com/docs"
            ]
        }),
        ("text", "APPENDICES", {
            "paragraphs": [
                "The appendix section contains supporting technical material related to the implementation of the project. It includes a data flow outline, logical storage structure, selected code snippets, and screenshot placeholder pages.",
                "These additions help explain how the project is organized internally and how the different technologies are connected."
            ],
            "bullets": []
        }),
        ("text", "DATA FLOW DIAGRAM (DFD)", {
            "paragraphs": [
                "The overall data flow of the application follows a clear sequence. The user selects or captures a plant image in the frontend. The image is then sent through a POST request to the Flask backend. The backend applies preprocessing, forwards the image to the CNN model, and returns the predicted class name. The frontend receives the response and shows the result page.",
                "This one-directional and predictable flow improves clarity and simplifies debugging."
            ],
            "bullets": [
                "User -> Scan Page -> Flask API -> Image Transform -> CNN Model -> Prediction -> Results Page"
            ]
        }),
        ("text", "DATABASE / STORAGE STRUCTURE", {
            "paragraphs": [
                "The current project uses Supabase for authentication-related storage and browser local storage for scan-history support. This approach is lightweight and suitable for a prototype while still demonstrating persistent session behavior and reusable scan data handling."
            ],
            "bullets": [
                "Supabase Auth: email, encrypted password, session data",
                "Local History: id, imageUrl, diseaseName, confidence, description, treatment, prevention, date, isHealthy"
            ]
        }),
        ("text", "APPENDIX NOTE - CLASS LABELS", {
            "paragraphs": [
                "The backend model is configured to return one out of 39 class labels. These labels include both healthy and diseased plant categories across crops such as apple, cherry, corn, grape, orange, peach, pepper, potato, strawberry, soybean, squash, and tomato.",
                "This class mapping is defined in the backend and is important because it converts the model output index into a readable disease name that can be displayed in the interface."
            ],
            "bullets": []
        }),
        ("code", "CODE SNIPPET - APP.PY", {"code": read_text(ROOT / "backend" / "App.py")}),
        ("code", "CODE SNIPPET - CNN.PY", {"code": read_text(ROOT / "backend" / "CNN.py")}),
        ("code", "CODE SNIPPET - APP.TSX", {"code": read_text(ROOT / "src" / "App.tsx")}),
        ("code", "CODE SNIPPET - INDEX.TSX", {"code": read_text(ROOT / "src" / "pages" / "Index.tsx")}),
        ("code", "CODE SNIPPET - LOGIN.TSX", {"code": read_text(ROOT / "src" / "pages" / "Login.tsx")}),
        ("code", "CODE SNIPPET - DASHBOARD.TSX", {"code": read_text(ROOT / "src" / "pages" / "Dashboard.tsx")}),
        ("code", "CODE SNIPPET - SCAN.TSX", {"code": read_text(ROOT / "src" / "pages" / "Scan.tsx")}),
        ("code", "CODE SNIPPET - RESULTS.TSX", {"code": read_text(ROOT / "src" / "pages" / "Results.tsx")}),
        ("code", "CODE SNIPPET - AUTHCONTEXT.TSX", {"code": read_text(ROOT / "src" / "contexts" / "AuthContext.tsx")}),
        ("placeholder", "SCREENSHOT - SCAN PAGE", {}),
        ("placeholder", "SCREENSHOT - RESULTS PAGE", {}),
        ("placeholder", "SCREENSHOT - HISTORY PAGE", {}),
    ]


def main() -> None:
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    for index, (kind, title, payload) in enumerate(build_pages(), start=1):
        if kind == "title":
            draw_title_page(c, title, index)
        elif kind == "text":
            draw_text_page(c, title, payload["paragraphs"], payload["bullets"], index)
        elif kind == "code":
            draw_code_page(c, title, payload["code"], index)
        elif kind == "placeholder":
            draw_placeholder_page(c, title, index)
    c.save()
    print(OUTPUT)
    print(f"pages={len(build_pages())}")


if __name__ == "__main__":
    main()
