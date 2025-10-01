import streamlit as st
import os
from dotenv import load_dotenv
from agents.unit_test_generator import SmartUnitTestGenerator
from agents.finance_sheet_analyzer import FinanceSheetAnalyzer
from agents.system_log_analyzer import SystemLogAnalyzer
import re
import pandas as pd
import datetime

load_dotenv()

# --- Modular, production-ready UI ---
def set_theme(dark_mode):
    # Modern glassmorphism theme with improved color contrast and wider layout
    if dark_mode:
        glass_bg = "rgba(34, 40, 49, 0.55)"
        card_bg = "rgba(44, 54, 73, 0.75)"
        text_color = "#F3F6FB"
        accent = "#4FC3F7"
        bg_gradient = "linear-gradient(135deg, #232a33 0%, #2b3140 100%)"
        input_bg = "rgba(44, 54, 73, 0.85)"
        input_border = "#4FC3F7"
        shadow = "0 8px 32px 0 rgba(31,38,135,0.25)"
        theme_selector = "body[data-theme='dark']"
    else:
        glass_bg = "rgba(255,255,255,0.45)"
        card_bg = "rgba(255,255,255,0.85)"
        text_color = "#232a33"
        accent = "#1976D2"
        bg_gradient = "linear-gradient(135deg, #e0e7ef 0%, #f5f7fa 100%)"
        input_bg = "rgba(255,255,255,0.65)"
        input_border = "#1976D2"
        shadow = "0 8px 32px 0 rgba(31,38,135,0.10)"
        theme_selector = "body[data-theme='light']"
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background: {bg_gradient} !important;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        }}
        .block-container {{
            background: {glass_bg} !important;
            border-radius: 20px !important;
            box-shadow: {shadow};
            padding: 2.5rem 2.5rem 2rem 2.5rem !important;
            max-width: 1200px !important;
            min-width: 700px !important;
        }}
        .glass-card {{
            background: {card_bg};
            color: {text_color} !important;
            box-shadow: {shadow};
            backdrop-filter: blur(18px) saturate(160%);
            -webkit-backdrop-filter: blur(18px) saturate(160%);
            border-radius: 20px;
            border: 1.5px solid {accent};
            padding: 2.5rem 2.5rem 2rem 2.5rem;
            margin-bottom: 2.5rem;
            max-width: 1000px;
            min-width: 600px;
            margin-left: auto;
            margin-right: auto;
            transition: box-shadow 0.2s;
        }}
        .glass-card:hover {{
            box-shadow: 0 12px 40px 0 {accent};
        }}
        .stSidebar {{
            background: {glass_bg} !important;
            border-radius: 18px !important;
            box-shadow: {shadow};
        }}
        .stTextInput, .stTextArea, .stFileUploader, .stSelectbox, .stDownloadButton, .stButton {{
            border-radius: 14px !important;
        }}
        .stTextInput>div>input, .stTextArea textarea {{
            background: {input_bg} !important;
            border: 1.5px solid {input_border} !important;
            color: {text_color} !important;
        }}
        .stDownloadButton>button, .stButton>button {{
            color: {text_color} !important;
            background: {glass_bg} !important;
            border: 1.5px solid {accent} !important;
            font-weight: 600;
        }}
        .stMarkdown, .stText, .stSubheader, .stHeader, .stTitle, .stInfo, .stSuccess, .stError, .stWarning {{
            color: {text_color} !important;
        }}
        .stAlert, .stInfo, .stSuccess, .stError, .stWarning {{
            border-radius: 14px !important;
        }}
        /* Modern scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: {accent};
            border-radius: 8px;
        }}
        /* Force text color in dark mode for all elements */
        {theme_selector} *, {theme_selector} .stMarkdown, {theme_selector} .stText, {theme_selector} .stSubheader, {theme_selector} .stHeader, {theme_selector} .stTitle, {theme_selector} .stInfo, {theme_selector} .stSuccess, {theme_selector} .stError, {theme_selector} .stWarning {{
            color: {text_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def sidebar_and_nav():
    if 'dark_mode' not in st.session_state:
        st.session_state['dark_mode'] = False
    st.sidebar.markdown("---")
    st.sidebar.write("### Theme")
    dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state['dark_mode'], key="dark_mode_toggle")
    st.session_state['dark_mode'] = dark_mode
    set_theme(dark_mode)
    st.sidebar.markdown("## 🧭 Navigation")
    nav_options = [
        ("Home", "🏠", "Home"),
        ("Smart Test Case Generator", "🧪", "Smart Test Case Generator"),
        ("Finance Sheet Analyzer", "📊", "Finance Sheet Analyzer"),
        ("System Log Analyzer", "📝", "System Log Analyzer")
    ]
    if 'selected_page' not in st.session_state or st.session_state['selected_page'] not in [k for k,_,_ in nav_options]:
        st.session_state['selected_page'] = "Home"
    # Glassmorphism button CSS with improved icon/text style
    glass_btn_css = f"""
    <style>
    .glass-nav-btn {{
        width: 100%;
        padding: 0.95rem 1.2rem;
        margin-bottom: 0.7rem;
        border: none;
        border-radius: 14px;
        background: {'rgba(44,54,73,0.65)' if dark_mode else 'rgba(255,255,255,0.65)'};
        color: {'#F3F6FB' if dark_mode else '#232a33'};
        font-size: 1.13rem;
        font-weight: 600;
        box-shadow: 0 4px 18px 0 rgba(31,38,135,0.10);
        backdrop-filter: blur(10px) saturate(160%);
        -webkit-backdrop-filter: blur(10px) saturate(160%);
        cursor: pointer;
        transition: background 0.18s, color 0.18s, box-shadow 0.18s;
        outline: none;
        border: 1.5px solid transparent;
        display: flex;
        align-items: center;
        gap: 0.7em;
        letter-spacing: 0.01em;
        text-align: left;
    }}
    .glass-nav-btn.selected {{
        background: {'rgba(79,195,247,0.85)' if dark_mode else 'rgba(25,118,210,0.12)'};
        color: {'#232a33' if dark_mode else '#1976D2'};
        border: 1.5px solid {'#4FC3F7' if dark_mode else '#1976D2'};
        box-shadow: 0 6px 24px 0 {'rgba(79,195,247,0.18)' if dark_mode else 'rgba(25,118,210,0.10)'};
    }}
    .glass-nav-btn .icon {{
        font-size: 1.35em;
        margin-right: 0.5em;
        display: flex;
        align-items: center;
    }}
    .glass-nav-btn .label {{
        font-size: 1.08em;
        font-weight: 600;
        letter-spacing: 0.01em;
        display: flex;
        align-items: center;
    }}
    </style>
    """
    st.sidebar.markdown(glass_btn_css, unsafe_allow_html=True)
    # Render glassy nav buttons using st.sidebar.button only
    for key, icon, label in nav_options:
        selected = st.session_state['selected_page'] == key
        btn_label = f'{icon} {label}'
        btn_kwargs = {"key": f"nav_btn_{key}"}
        if selected:
            st.sidebar.markdown(f'<div class="glass-nav-btn selected"><span class="icon">{icon}</span><span class="label">{label}</span></div>', unsafe_allow_html=True)
        else:
            if st.sidebar.button(btn_label, **btn_kwargs):
                st.session_state['selected_page'] = key
    return st.session_state['selected_page']


def home_ui():
    st.markdown("<h1>🏠 Welcome to AI Agents Workspace</h1>", unsafe_allow_html=True)
    st.markdown("""
    This workspace lets you explore and use different AI agents for software QA and automation.<br>
    <ul>
    <li>Use the sidebar to navigate to available agents.</li>
    <li>Each agent provides a specialized interface and workflow.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("<p>Select an agent from the sidebar to get started.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def test_case_generator_ui():
    st.markdown("<h1>🤖 Smart Test Case Generator</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome! As a Senior AI Developer, I've built this tool to streamline your QA process.<br>
    Provide your software requirements below, and my crew of AI agents will generate a comprehensive set of test cases for you.
    """, unsafe_allow_html=True)
    st.sidebar.header("How to Use")
    st.sidebar.info(
        """
        1.  **Enter Requirements**: You can either paste the requirements directly into the text area or upload a `.txt` or `.md` file.
        2.  **Generate**: Click the 'Generate Smart Test Cases' button.
        3.  **Review**: The AI crew will analyze the requirements and generate test cases, which will appear in the main panel.
        """
    )
    st.sidebar.header("About the AI Crew")
    st.sidebar.markdown(
        """
        -   **Requirements Analyst**: This agent first dissects your requirements into core functionalities and user stories.
        -   **Test Case Generator**: This agent takes the analysis and writes detailed positive, negative, and edge-case tests.
        """
    )
    if 'testcase_history' not in st.session_state:
        st.session_state['testcase_history'] = []
    st.sidebar.markdown('---')
    st.sidebar.subheader('🕑 History')
    clear_tc_hist = st.sidebar.button('Clear History', key='clear_testcase_history_sidebar')
    if clear_tc_hist:
        st.session_state['testcase_history'] = []
    history_style = """
    <style>
    .sidebar-history-panel {
        max-height: 250px;
        overflow-y: auto;
        border: 1px solid #888;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: %s;
        color: %s;
    }
    .sidebar-history-user { font-weight: bold; }
    .sidebar-history-agent { margin-top: 2px; }
    </style>
    """ % ("#232323" if st.session_state.get('dark_mode', False) else "#f5f5f5", "#E0E0E0" if st.session_state.get('dark_mode', False) else "#212121")
    st.sidebar.markdown(history_style, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-history-panel">', unsafe_allow_html=True)
    for entry in reversed(st.session_state['testcase_history']):
        st.sidebar.markdown(f'<div class="sidebar-history-entry"><div class="sidebar-history-timestamp">{entry["timestamp"]}</div><div class="sidebar-history-user">User input: <code>{entry["user_input"]}</code></div><div class="sidebar-history-agent"><b>Agent:</b> {entry["agent_response"]}</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    requirements_text = st.text_area("Enter Software Requirements Here:", height=200, key="requirements_text_area")
    uploaded_file = st.file_uploader("Or upload a requirements file (.txt, .md)", type=['txt', 'md'], key="requirements_file_uploader")
    if uploaded_file is not None:
        try:
            string_data = uploaded_file.getvalue().decode("utf-8")
            requirements_text = string_data
            st.info("File content loaded into the text area.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    def format_test_cases(raw_output):
        pattern = re.compile(r"Test Case ID:.*?(?=Test Case ID:|$)", re.DOTALL)
        cases = pattern.findall(raw_output)
        if cases:
            table = (
                "| Test Case ID | Title | Preconditions | Test Steps | Input Data | Expected Results | Actual Result |\n"
                "|---|---|---|---|---|---|---|\n"
            )
            for case in cases:
                def extract(field):
                    m = re.search(rf"{field}:\s*(.*)", case)
                    return m.group(1).strip() if m else ""
                table += f"| {extract('Test Case ID')} | {extract('Title')} | {extract('Preconditions')} | {extract('Test Steps')} | {extract('Input Data')} | {extract('Expected Results')} | {extract('Actual Result')} |\n"
            return table
        return raw_output
    if st.button("Generate Smart Test Cases", key="generate_test_cases_btn"):
        if not requirements_text.strip():
            st.error("Please enter or upload some requirements before generating.")
        else:
            with st.spinner('🤖 AI Crew is analyzing requirements and crafting test cases... This may take a moment.'):
                try:
                    agent = SmartUnitTestGenerator()
                    result = agent.generate_test_cases(requirements_text)
                    formatted_result = format_test_cases(result)
                    st.success("Test cases generated successfully!")
                    st.markdown(formatted_result)
                    st.download_button(
                        label="Download Test Cases",
                        data=formatted_result,
                        file_name="test_cases.md",
                        mime="text/markdown"
                    )
                    st.session_state['testcase_history'].append({
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "user_input": requirements_text[:100].replace('\n', ' ') + ("..." if len(requirements_text) > 100 else ""),
                        "agent_response": formatted_result[:200] + ("..." if len(formatted_result) > 200 else "")
                    })
                except Exception as e:
                    st.error(f"An error occurred while running the AI crew: {e}")
                    st.error("Please ensure the Ollama Docker container is running and accessible.")
    st.markdown('</div>', unsafe_allow_html=True)


def finance_analyzer_ui():
    st.markdown("<h1>📊 Finance Sheet Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("""
    Upload your Excel financial sheet below. The AI agent will review for anomalies, summarize expenses, and highlight trends or inconsistencies in your financial data.
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"], key="finance_file_uploader")
    regenerate = False
    # --- Sidebar: How to Use & About the AI Crew ---
    st.sidebar.header("How to Use")
    st.sidebar.info(
        """
1. **Upload File**: Click 'Upload Excel File' and select your `.xlsx` financial sheet.
2. **Analyze**: The AI agent will automatically process your data and display KPIs, charts, and insights.
3. **Regenerate**: Click 'Regenerate Analysis' to re-run the analysis after uploading a new file.
        """
    )
    st.sidebar.header("About the AI Crew")
    st.sidebar.markdown(
        """
- **Financial Data Reader**: Detects and reads all columns, including custom names like 'Credit (Inflow)' and 'Debit (Outflow)'.
- **KPI & Trend Analyzer**: Calculates inflows, outflows, net balance, and trends from your data.
- **Dashboard Designer**: Creates modern, accessible charts and tables for a clear financial overview.
- **LLM Insights Agent**: Uses local Ollama to generate actionable insights and recommendations from your data.
        """
    )
    # --- Sidebar: History Panel ---
    if 'finance_history' not in st.session_state:
        st.session_state['finance_history'] = []
    st.sidebar.markdown('---')
    st.sidebar.subheader('🕑 History')
    clear_hist = st.sidebar.button('Clear History', key='clear_finance_history_sidebar')
    if clear_hist:
        st.session_state['finance_history'] = []
    history_style = """
    <style>
    .sidebar-history-panel {
        max-height: 250px;
        overflow-y: auto;
        border: 1px solid #888;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: %s;
        color: %s;
    }
    .sidebar-history-entry { margin-bottom: 12px; }
    .sidebar-history-timestamp { font-size: 11px; color: #888; }
    .sidebar-history-user { font-weight: bold; }
    .sidebar-history-agent { margin-top: 2px; }
    </style>
    """ % ("#232323" if st.session_state.get('dark_mode', False) else "#f5f5f5", "#E0E0E0" if st.session_state.get('dark_mode', False) else "#212121")
    st.sidebar.markdown(history_style, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-history-panel">', unsafe_allow_html=True)
    for entry in reversed(st.session_state['finance_history']):
        st.sidebar.markdown(f'<div class="sidebar-history-entry"><div class="sidebar-history-timestamp">{entry["timestamp"]}</div><div class="sidebar-history-user">User uploaded: <code>{entry["user_input"]}</code></div><div class="sidebar-history-agent"><b>Agent:</b> {entry["agent_response"]}</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    # --- Main Analysis ---
    if uploaded_file is not None:
        if st.button("Regenerate Analysis", key="regenerate_finance_analysis"):
            regenerate = True
        try:
            import matplotlib.pyplot as plt
            df = pd.read_excel(uploaded_file)
            st.success("File uploaded and read successfully!")
            st.dataframe(df)
            from agents.finance_sheet_analyzer import FinanceSheetAnalyzer
            analyzer = FinanceSheetAnalyzer()
            if regenerate or st.session_state.get('finance_first_run', True):
                with st.spinner('Analyzing financial data...'):
                    result = analyzer.analyze(df)
                st.session_state['finance_result'] = result
                st.session_state['finance_first_run'] = False
                # --- Add to history ---
                st.session_state['finance_history'].append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user_input": uploaded_file.name,
                    "agent_response": result.get('llm_analysis', 'No response')
                })
            else:
                result = st.session_state.get('finance_result', {})
            # --- Modern Dashboard UI ---
            st.markdown("<hr style='margin:24px 0;'>", unsafe_allow_html=True)
            st.markdown("## 📈 Key Financial KPIs")
            kpi_cols = st.columns(4)
            kpi_cols[0].markdown(f"<div style='background:#e3f2fd;padding:18px;border-radius:10px;text-align:center;'><span style='font-size:18px;font-weight:bold;'>Total Inflows</span><br><span style='font-size:28px;color:#1976d2;font-weight:bold;'>{result.get('total_inflows', 'N/A')}</span></div>", unsafe_allow_html=True)
            kpi_cols[1].markdown(f"<div style='background:#ffebee;padding:18px;border-radius:10px;text-align:center;'><span style='font-size:18px;font-weight:bold;'>Total Outflows</span><br><span style='font-size:28px;color:#d32f2f;font-weight:bold;'>{result.get('total_outflows', 'N/A')}</span></div>", unsafe_allow_html=True)
            kpi_cols[2].markdown(f"<div style='background:#e8f5e9;padding:18px;border-radius:10px;text-align:center;'><span style='font-size:18px;font-weight:bold;'>Net Balance</span><br><span style='font-size:28px;color:#388e3c;font-weight:bold;'>{result.get('net_balance', 'N/A')}</span></div>", unsafe_allow_html=True)
            kpi_cols[3].markdown(f"<div style='background:#fffde7;padding:18px;border-radius:10px;text-align:center;'><span style='font-size:18px;font-weight:bold;'>Monthly Avg</span><br><span style='font-size:28px;color:#fbc02d;font-weight:bold;'>{result.get('monthly_average', 'N/A')}</span></div>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:24px 0;'>", unsafe_allow_html=True)
            st.markdown("## 🗂️ Category Breakdown")
            breakdown_cols = st.columns(2)
            breakdown_cols[0].markdown("**Top 3 Inflow Categories:**")
            breakdown_cols[0].table(result.get('top_inflow_categories', []))
            breakdown_cols[1].markdown("**Top 3 Outflow Categories:**")
            breakdown_cols[1].table(result.get('top_outflow_categories', []))
            st.markdown("**Category Contribution to Inflows:**")
            st.bar_chart(result.get('category_inflows', {}))
            st.markdown("**Category Consumption of Outflows:**")
            st.bar_chart(result.get('category_outflows', {}))
            # Pie charts for inflow and outflow breakdowns
            import matplotlib.pyplot as plt
            inflow_data = result.get('category_inflows', {})
            outflow_data = result.get('category_outflows', {})
            if inflow_data:
                st.markdown("**Inflow Category Breakdown (Pie Chart):**")
                fig1, ax1 = plt.subplots()
                ax1.pie(list(inflow_data.values()), labels=list(inflow_data.keys()), autopct='%1.1f%%', startangle=90)
                ax1.axis('equal')
                st.pyplot(fig1)
            if outflow_data:
                st.markdown("**Outflow Category Breakdown (Pie Chart):**")
                fig2, ax2 = plt.subplots()
                ax2.pie(list(outflow_data.values()), labels=list(outflow_data.keys()), autopct='%1.1f%%', startangle=90)
                ax2.axis('equal')
                st.pyplot(fig2)
            st.markdown("<hr style='margin:24px 0;'>", unsafe_allow_html=True)
            st.markdown("## 📊 Yearly Trends")
            trends_df = result.get('yearly_trends', None)
            if trends_df is not None and not trends_df.empty:
                st.line_chart(trends_df)
            else:
                st.info("No multi-year trend data available.")
            st.markdown("<hr style='margin:24px 0;'>", unsafe_allow_html=True)
            st.markdown("## 💡 Insights & Observations")
            st.markdown(result.get('insights', 'No insights generated.'), unsafe_allow_html=True)
            st.markdown("## 📝 Recommendations")
            st.markdown(result.get('recommendations', 'No recommendations generated.'), unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("### 📊 Dashboard Preview (Excel)")
            st.markdown("- Pivot tables by Category & Year\n- KPI summary cards\n- Charts for trends & breakdowns\n- Downloadable Excel dashboard (coming soon)")
            if 'llm_analysis' in result:
                llm_output = result['llm_analysis'].strip()
                if llm_output and llm_output != '**':
                    st.markdown("<div style='background-color:#f5f5f5;padding:18px;border-radius:10px;border:1px solid #bdbdbd;margin-bottom:18px;'>", unsafe_allow_html=True)
                    st.subheader("AI-Powered Financial Insights")
                    st.markdown(llm_output, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            if 'error' in result:
                st.error(f"Analyzer error: {result['error']}")
        except Exception as e:
            st.error(f"Error processing file: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


def system_log_analyzer_ui():
    st.markdown("<h1>📝 System Log Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("""
    Upload your system log file below. The AI agent will analyze the log for errors, warnings, and other significant events.
    """, unsafe_allow_html=True)
    # --- Sidebar: How to Use & About the AI Crew ---
    st.sidebar.header("How to Use")
    st.sidebar.info(
        """
1. **Paste or Upload Logs**: Paste your log text or upload a `.log` or `.txt` file.
2. **Analyze**: Click 'Analyze Logs' to let the AI agent review your logs for errors, warnings, and anomalies.
3. **Review**: Explore the dashboard for summaries, tables, and actionable recommendations.
        """
    )
    st.sidebar.header("About the AI Crew")
    st.sidebar.markdown(
        """
- **Log Pattern Detector**: Identifies recurring errors, spikes, and unusual patterns.
- **Root Cause Analyst**: Suggests likely causes and next steps for major issues.
- **LLM Insights Agent**: Uses Llama 3.1 to generate a professional, actionable dashboard from your logs.
        """
    )
    # --- Sidebar: History Panel ---
    if 'log_history' not in st.session_state:
        st.session_state['log_history'] = []
    st.sidebar.markdown('---')
    st.sidebar.subheader('🕑 History')
    clear_hist = st.sidebar.button('Clear History', key='clear_log_history_sidebar')
    if clear_hist:
        st.session_state['log_history'] = []
    history_style = """
    <style>
    .sidebar-history-panel {
        max-height: 250px;
        overflow-y: auto;
        border: 1px solid #888;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: %s;
        color: %s;
    }
    .sidebar-history-entry { margin-bottom: 12px; }
    .sidebar-history-timestamp { font-size: 11px; color: #888; }
    .sidebar-history-user { font-weight: bold; }
    .sidebar-history-agent { margin-top: 2px; }
    </style>
    """ % ("#232323" if st.session_state.get('dark_mode', False) else "#f5f5f5", "#E0E0E0" if st.session_state.get('dark_mode', False) else "#212121")
    st.sidebar.markdown(history_style, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-history-panel">', unsafe_allow_html=True)
    for entry in reversed(st.session_state['log_history']):
        st.sidebar.markdown(f'<div class="sidebar-history-entry"><div class="sidebar-history-timestamp">{entry["timestamp"]}</div><div class="sidebar-history-user">User input: <code>{entry["user_input"]}</code></div><div class="sidebar-history-agent"><b>Agent:</b> {entry["agent_response"]}</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    log_text = st.text_area("Paste system log text here:", height=200, key="log_text_area")
    uploaded_file = st.file_uploader("Or upload a log file (.log, .txt)", type=["log", "txt"], key="log_file_uploader")
    if uploaded_file is not None:
        try:
            string_data = uploaded_file.getvalue().decode("utf-8")
            log_text = string_data
            st.info("File content loaded into the text area.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    def parse_sections(md):
        import re
        # Split by Markdown headers (## or ###)
        sections = re.split(r'(^##+ .*$)', md, flags=re.MULTILINE)
        parsed = []
        if len(sections) == 1:
            return [("Report", md)]
        i = 0
        while i < len(sections):
            if sections[i].startswith('##'):
                title = sections[i].replace('#', '').strip()
                content = sections[i+1] if i+1 < len(sections) else ''
                parsed.append((title, content.strip()))
                i += 2
            else:
                i += 1
        return parsed

    def extract_tables(md):
        import re
        import pandas as pd
        tables = []
        pattern = r'(\|.+\|\n\|[\-\| ]+\|\n(?:\|.*\|\n)+)'
        for match in re.finditer(pattern, md):
            table_md = match.group(1)
            try:
                df = pd.read_csv(pd.compat.StringIO(table_md), sep='|', engine='python', skipinitialspace=True)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                tables.append(df)
            except Exception:
                continue
        return tables

    def plot_error_breakdown(md):
        import re
        import pandas as pd
        # Look for a table with Error/Warning breakdown
        pattern = r'(\|.+\|\n\|[\-\| ]+\|\n(?:\|.*\|\n)+)'
        for match in re.finditer(pattern, md):
            table_md = match.group(1)
            try:
                df = pd.read_csv(pd.compat.StringIO(table_md), sep='|', engine='python', skipinitialspace=True)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                # If table has 'Error' or 'Warning' in columns, plot
                if any(col.lower() in ['error', 'errors', 'warning', 'warnings', 'count'] for col in df.columns):
                    st.bar_chart(df.set_index(df.columns[0]))
            except Exception:
                continue

    if st.button("Analyze Logs", key="analyze_logs_btn"):
        if not log_text.strip():
            st.error("Please enter or upload some log text before analyzing.")
        else:
            with st.spinner('🤖 AI Crew is analyzing your logs...'):
                agent = SystemLogAnalyzer()
                result = agent.analyze(log_text)
                llm_report = result
                st.success("Log analysis completed!")
                # Parse and display sections
                for title, content in parse_sections(llm_report):
                    with st.expander(title, expanded=(title.lower().startswith('executive') or title.lower().startswith('key'))):
                        # Try to extract and display tables
                        tables = extract_tables(content)
                        if tables:
                            for df in tables:
                                st.table(df)
                        else:
                            st.markdown(content)
                        # Try to plot error/warning breakdowns
                        plot_error_breakdown(content)
                st.download_button(
                    label="Download LLM Report",
                    data=llm_report,
                    file_name="log_analysis_report.md",
                    mime="text/markdown"
                )
                # --- Add to history ---
                if 'log_history' not in st.session_state:
                    st.session_state['log_history'] = []
                st.session_state['log_history'].append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user_input": log_text[:100].replace('\n', ' ') + ("..." if len(log_text) > 100 else ""),
                    "agent_response": llm_report[:200] + ("..." if len(llm_report) > 200 else "")
                })
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    selected_page = sidebar_and_nav()
    if selected_page == "Home":
        home_ui()
    elif selected_page == "Smart Test Case Generator":
        test_case_generator_ui()
    elif selected_page == "Finance Sheet Analyzer":
        finance_analyzer_ui()
    elif selected_page == "System Log Analyzer":
        system_log_analyzer_ui()


if __name__ == "__main__":
    main()
