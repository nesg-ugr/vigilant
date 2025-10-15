
# VIGILANT

**Verification of Intent and Generation of Intelligent Logic for Automated actions against Network and systems security Threats**

VIGILANT is a research-driven, open framework to **analyze, diagnose, and respond to security incidents using Large Language Models (LLMs)**. It focuses on **natural-language interaction**, **encoding heterogeneous security data (logs, NIDS alerts, network traces/PCAP)**, **intent-to-configuration translation**, and **safe validation of proposed actions in simulation** before touching production.

<p align="center">
  <a href="https://nesg.ugr.es/projects/vigilant" target="_blank">
    <img src="logo.png" alt="VIGILANT Logo" width="350">
  </a>
</p>

<p align="center">
<a href="https://nesg.ugr.es" target="_blank"><img alt="NESG-UGR" src="https://img.shields.io/badge/NESG-UGR-blue"></a>
<img alt="Status" src="https://img.shields.io/badge/status-research--prototype-yellow">
<img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-green">
</p>

---

## ⚙️ Key capabilities

- **Data ingestion & encoding** of heterogeneous security sources (logs, IDS alerts, network traces/PCAP) into LLM-interpretable tokens/text.  
- **Natural-language queries** to accelerate incident inspection/diagnosis.  
- **Intent-based actions**: translate analyst intentions (in plain English/Spanish) into concrete security configurations (e.g., firewall policies).  
- **Action verification**: automatically validate proposed configurations in a **simulated environment** (a “digital twin” subset) before optional deployment.  
- **Fine-tuning/RAG options** to specialize models for cybersecurity tasks and external tool enrichment (e.g., CTI, visualization).

---

## 🏗️ Architecture (high-level)

<p align="center">
  <a href="docs/architecture.png" target="_blank">
    <img src="docs/architecture.png" alt="VIGILANT Architecture Overview" width="720">
  </a>
  <br/>
  <em>Figure: VIGILANT high-level architecture. Click to view full size. (You can replace with docs/architecture.svg if preferred.)</em>
</p>

1. **System inputs**: analyst prompts + security data (logs, alerts, PCAP).  
2. **Data encoding**: transform raw sources into representative tokens/text for the LLM (unimodal) and explore **multimodal** paths for raw formats when feasible.  
3. **Request adaptation**: decompose complex prompts into sub-queries and iterate.  
4. **Response aggregation**: synthesize sub-answers into a coherent diagnosis.  
5. **Intention → configuration**: map analyst intentions to actionable configs (e.g., iptables rules).  
6. **Simulation & validation**: test configurations in a controlled environment before real deployment.  
7. **External tool integration**: CTI lookups, plots, dashboards, etc.

> **Note:** Place the image at `docs/architecture.png` (recommended: 1600×1000, PNG or SVG). Keep any sensitive details out of the diagram.

---

## 📁 Repository layout

:construction: *To be completed*

---

## 🚀 Quick start

:construction: *To be completed*

---

## 💻 Usage

:construction: *To be completed*

---

## 🤝 Contributing

We welcome issues, discussions, and PRs!

1. Open an issue describing your proposal/bug with minimal repro.  
2. Follow the style checks: `ruff`, `black`, and `mypy` where applicable.  
3. Add/extend tests for new functionality.  
4. Ensure no sensitive data is committed; use synthetic/redacted samples only.

---

## 📚 Publications

The following list gathers **scientific publications derived from or related to the VIGILANT project**.  
Please cite the relevant paper(s) when using any portion of this repository.  
A full and updated list is maintained in [`publications.bib`](./publications.bib).

* R. García-Peñas, R. A. Rodríguez-Gómez, and G. Maciá-Fernández, “Characterizing Internet Background Traffic from a Spain-Based Network Telescope,” Computers & Security, vol. 159, p. 104693, Dec. 2025, [doi: 10.1016/j.cose.2025.104693](https://www.sciencedirect.com/science/article/pii/S0167404825003827).

```bibtex
@article{garcia-penas_characterizing_2025,
	title = {Characterizing {Internet} {Background} {Traffic} from a {Spain}-{Based} {Network} {Telescope}},
	volume = {159},
	issn = {0167-4048},
	url = {https://www.sciencedirect.com/science/article/pii/S0167404825003827},
	doi = {10.1016/j.cose.2025.104693},
	urldate = {2025-10-13},
	journal = {Computers \& Security},
	author = {García-Peñas, Rodolfo and Rodríguez-Gómez, Rafael A. and Maciá-Fernández, Gabriel},
	month = dec,
	year = {2025},
	keywords = {Backscatter, IBN (Internet Background Noise), IBR (Internet Background Radiation), Network telescope},
	pages = {104693}
}
```

---

## 💡 Funding & acknowledgments

This work is part of the **VIGILANT** research project (Knowledge Generation Projects 2024 – Oriented Research Type B, Spanish Ministry of Science, Innovation and Universities, PID2024-161902OB-I00).  
We acknowledge the **NESG (TIC-233)** group and collaborating partners, and plan public releases of preprocessing, benchmarks, models, and front/back-end artifacts to foster reproducible research and SME adoption.

---

## 🧾 License

Released under the **Apache License 2.0**.  
See the `LICENSE` file for details.

---

**Maintainers**

- **NESG – Network Engineering & Security Group (UGR)**  
  PIs: **Pedro García Teodoro** (pgteodor [at] ugr [dot] es)  & **Roberto Magán Carrión** (rmagan [at] ugr [dot] es)  
  Website: [https://nesg.ugr.es](https://nesg.ugr.es)
