# Domain Profile

## Field

**Primary:** AI Research / Marketing Analytics
**Adjacent subfields:** Machine Learning, Customer Relationship Management (CRM), Predictive Modeling, Econometrics

---

## Target Journals (ranked by tier)

| Tier | Journals |
|------|----------|
| Top-tier | Marketing Science, Management Science, Journal of Marketing Research |
| High field | Journal of Marketing, MIS Quarterly, Decision Support Systems |
| Specialized AI | Journal of Machine Learning Research, NeurIPS, ICML (for methodological papers) |
| Applied | Journal of Retailing, Journal of Interactive Marketing |

---

## Common Data Sources

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| IBM Telco Customer Churn | CRM | Public (Kaggle) | Primary dataset. Baseline for churn prediction with demographic and service features. |

---

## Common Identification Strategies

| Strategy | Typical Application | Key Assumption to Defend |
|----------|-------------------|------------------------|
| Predictive ML with XAI | Explainable Churn probability estimation | SHAP values accurately reflect true feature contributions |
| Profit-driven Evaluation | Cost-benefit evaluation matrices | Financial assumptions (retention cost framework) are realistic |
| Decision Support System (BI) | Streamlit BI tool for Strategic Planning | Offline simulations using static data hold true for live BI use |

---

## Field Conventions

- **Baseline Comparison:** Always compare against Random Forest or Logistic Regression.
- **Evaluation Metrics:** Accuracy is insufficient; report AUC-ROC, Recall at top X%, and F1-score.
- **Business Impact:** Translate model performance into monetary value (Customer Lifetime Value).
- **Interpretability:** Use SHAP or LIME for complex models (Black-box models require explanation).

---

## Notation Conventions

| Symbol | Meaning | Anti-pattern |
|--------|---------|-------------|
| $y_i \in \{0, 1\}$ | Binary churn indicator | Avoid using continuous $y$ without threshold |
| $\hat{y}_i$ | Predicted probability / Score | |
| $\phi_j$ | SHAP value for feature $j$ | |
| $C(TP, FP, FN, TN)$ | Cost-benefit matrix | Assuming uniform misclassification costs |

---

## Seminal References

| Paper | Why It Matters |
|-------|---------------|
| Ascarza (2018) | Retention Futility - Moving from churn prediction to response prediction |
| Verbeke et al. (2012) | Profit-driven churn prediction |
| Ganin et al. (2016) | Domain-Adversarial Training of Neural Networks |

---

## Paper Author Team

| Author | Foundational on |
|--------|----------------|
| [Author Name] | [Focus Area] |

---

## Field-Specific Referee Concerns

- Class Imbalance: How was it handled (SMOTE, weighting, etc.)?
- Data Leakage: Are features derived from the future (post-churn event)?
- Model Complexity: Is the deep learning approach significantly better than a simpler XGBoost?
- Dynamic Nature: How does the model handle changing customer behavior over time?
