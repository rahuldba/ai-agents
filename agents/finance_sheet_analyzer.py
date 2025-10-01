import pandas as pd
from llm.llama_client_Test_and_Finance import LlamaClient

class FinanceSheetAnalyzer:
    """
    Goal: Provide actionable, visually rich financial analysis for uploaded transaction sheets (Excel/CSV).
    Backstory: You are a professional financial analyst with expertise in dashboard design and business reporting. Your mission is to help users understand their financial health, spot trends, and optimize spending/income using clear KPIs, breakdowns, and modern visualizations.
    """
    def __init__(self):
        self.llm = LlamaClient()
        self.goal = (
            "Empower users to make informed financial decisions by providing comprehensive, actionable, and visually engaging analysis of uploaded transaction sheets (Excel/CSV). "
            "Deliver clear KPIs, category breakdowns, trends, and strategic recommendations, all presented in a modern dashboard format."
        )
        self.backstory = (
            "You are a senior financial analyst with a background in business intelligence, data visualization, and executive reporting. "
            "You have helped hundreds of organizations optimize their financial operations, spot risks, and identify growth opportunities. "
            "Your approach combines deep analytical rigor with a talent for making complex data accessible and actionable for decision-makers. "
            "You believe every financial report should tell a story, highlight what matters, and inspire confident action."
        )

    def analyze(self, df):
        result = {}
        # Validate input
        if df is None or df.empty:
            result['error'] = "No data found in uploaded sheet. Please check your file."
            return result
        try:
            col_map = {c.lower(): c for c in df.columns}
            result['debug_columns'] = str(list(df.columns))
            # Robust partial matching for inflow/outflow columns
            inflow_col = None
            outflow_col = None
            for col in df.columns:
                col_lower = col.lower()
                if inflow_col is None and ("credit" in col_lower or "inflow" in col_lower or "income" in col_lower):
                    inflow_col = col
                if outflow_col is None and ("debit" in col_lower or "outflow" in col_lower or "expense" in col_lower):
                    outflow_col = col
                if inflow_col and outflow_col:
                    break
            # Fallback to exact/legacy logic if not found
            if not inflow_col:
                inflow_col = next((col_map[k] for k in ['credit', 'inflow', 'income', 'amount'] if k in col_map), None)
            if not outflow_col:
                outflow_col = next((col_map[k] for k in ['debit', 'outflow', 'expense', 'amount'] if k in col_map), None)
            category_col = next((col_map[k] for k in ['category', 'type', 'group'] if k in col_map), None)
            month_col = next((col_map[k] for k in ['month', 'period'] if k in col_map), None)
            year_col = next((col_map[k] for k in ['year', 'fiscal_year'] if k in col_map), None)
            # KPIs
            if inflow_col and outflow_col and inflow_col != outflow_col:
                inflow = pd.to_numeric(df[inflow_col], errors='coerce').sum()
                outflow = pd.to_numeric(df[outflow_col], errors='coerce').sum()
                result['total_inflows'] = inflow
                result['total_outflows'] = outflow
                result['net_balance'] = inflow - outflow
            elif inflow_col:
                inflow = pd.to_numeric(df[df[inflow_col] > 0][inflow_col], errors='coerce').sum()
                outflow = -pd.to_numeric(df[df[inflow_col] < 0][inflow_col], errors='coerce').sum()
                result['total_inflows'] = inflow
                result['total_outflows'] = outflow
                result['net_balance'] = inflow - outflow
            else:
                result['total_inflows'] = result['total_outflows'] = result['net_balance'] = 0
            # Monthly average
            if month_col and inflow_col and outflow_col and inflow_col != outflow_col:
                monthly_avg = (df.groupby(month_col)[inflow_col].sum() - df.groupby(month_col)[outflow_col].sum()).mean()
                result['monthly_average'] = monthly_avg
            else:
                result['monthly_average'] = 'N/A'
            # Category breakdowns
            if category_col and inflow_col and outflow_col and inflow_col != outflow_col:
                inflow_by_cat = df.groupby(category_col)[inflow_col].sum().sort_values(ascending=False)
                outflow_by_cat = df.groupby(category_col)[outflow_col].sum().sort_values(ascending=False)
                result['category_inflows'] = inflow_by_cat.to_dict()
                result['category_outflows'] = outflow_by_cat.to_dict()
                result['top_inflow_categories'] = inflow_by_cat.head(3).reset_index().values.tolist()
                result['top_outflow_categories'] = outflow_by_cat.head(3).reset_index().values.tolist()
            else:
                result['category_inflows'] = result['category_outflows'] = {}
                result['top_inflow_categories'] = result['top_outflow_categories'] = []
            # Yearly trends
            if year_col and inflow_col and outflow_col and inflow_col != outflow_col:
                yearly = df.groupby(year_col).agg({inflow_col: 'sum', outflow_col: 'sum'})
                yearly['Net'] = yearly[inflow_col] - yearly[outflow_col]
                result['yearly_trends'] = yearly
            else:
                result['yearly_trends'] = pd.DataFrame()
            # Insights & recommendations
            result['insights'] = "<ul><li>Profitability status: <b>{}</b></li><li>Expense hotspots: <b>{}</b></li><li>Cash flow risks: <b>{}</b></li></ul>".format(
                "Profitable" if result.get('net_balance', 0) > 0 else "Loss", 
                ', '.join([str(x[0]) for x in result.get('top_outflow_categories', [])]) if result.get('top_outflow_categories', []) else "N/A", 
                "High" if result.get('total_outflows', 0) > result.get('total_inflows', 0) else "Low")
            result['recommendations'] = "<ul><li>Review top expense categories for optimization.</li><li>Monitor monthly averages for unusual spikes.</li><li>Consider strategies to increase inflows.</li></ul>"
            # Improved LLM prompt for dashboard and visualization
            dashboard_instruction = (
                "You are a senior financial analyst and dashboard designer."
                " Your task is to analyze the provided financial transaction data and deliver a report that includes:"
                "\n- Key Financial KPIs (Total Inflows, Total Outflows, Net Balance, Monthly Average)"
                "\n- Category-wise breakdowns (Top inflow/outflow categories, category contributions)"
                "\n- Yearly and monthly trends (growth, decline, profitability timeline)"
                "\n- Insights and observations (profitability status, expense hotspots, cash flow risks, ROI analysis)"
                "\n- Actionable recommendations (optimization, strategy, risk mitigation)"
                "\n- Step-by-step instructions for building a dashboard in Excel:"
                "\n  * Use pivot tables for category, month, and year analysis"
                "\n  * Create summary cards for KPIs"
                "\n  * Add bar, pie, and line charts for trends and breakdowns"
                "\n  * Highlight key findings and suggest next steps"
                "\nBe concise but analytical, and always interpret the numbers for business impact."
            )
            prompt = (
                f"Goal: {self.goal}\nBackstory: {self.backstory}\n"
                "Instructions: " + dashboard_instruction + "\n"
                "Data (first 50 rows):\n" + df.head(50).to_string(index=False)
            )
            llm_response = self.llm.query(prompt)
            llm_output = llm_response.strip()
            if not llm_output or llm_output == '**':
                llm_output = "No clear financial insights detected. Please review your data for completeness, but here is a general suggestion: Consider adding more transaction details or categories for deeper analysis."
            result['llm_analysis'] = llm_output
            return result
        except Exception as e:
            result['error'] = str(e)
            return result
