#!/usr/bin/env python3
"""Standalone script to download a collection of scientific PDF papers.

Downloads all papers listed in `papers` into ./pdf_repository/,
using a thread pool for concurrency, realistic browser headers to avoid
403s from academic repositories, and skips files that already exist.
"""

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

OUTPUT_DIR = "pdf_repository"
MAX_WORKERS = 5
TIMEOUT_SECONDS = 15

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

papers = [
    # Data Science, Machine Learning & AI Foundations
    {"title": "Hey_2009_The_Fourth_Paradigm", "url": "https://www.microsoft.com/en-us/research/wp-content/uploads/2009/10/Fourth_Paradigm.pdf"},
    {"title": "Tukey_1962_The_Future_of_Data_Analysis", "url": "http://www.mat.ufrgs.br/~viali/estatistica/mat2274/material/textos/2237638.pdf"},
    {"title": "McCarthy_1955_Dartmouth_AI_Proposal", "url": "http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf"},
    {"title": "Samuel_1959_Machine_Learning_Checkers", "url": "https://people.csail.mit.edu/brooks/idocs/Samuel.pdf"},
    {"title": "Rumelhart_1986_Backpropagating_Errors", "url": "https://www.iro.umontreal.ca/~vincentp/ift3395/lectures/backprop_old.pdf"},
    {"title": "Glorot_Bengio_2010_Training_Deep_Feedforward_Neural_Networks", "url": "https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf"},
    {"title": "Hochreiter_Schmidhuber_1997_LSTM", "url": "https://direct.mit.edu/neco/article-pdf/9/8/1735/813796/neco.1997.9.8.1735.pdf"},
    {"title": "Chiappa_2017_Recurrent_Environment_Simulators", "url": "https://arxiv.org/pdf/1704.02254.pdf"},
    {"title": "Rudin_2019_Stop_Explaining_Black_Box_Models", "url": "https://arxiv.org/pdf/1811.10154.pdf"},
    {"title": "Cranmer_2020_Discovering_Symbolic_Models", "url": "https://arxiv.org/pdf/2006.11287.pdf"},

    # AI Impact, Climate & Governance
    {"title": "Vinuesa_2020_AI_in_Sustainable_Development_Goals", "url": "https://www.nature.com/articles/s41467-019-14108-y.pdf"},
    {"title": "Vinuesa_Sirmacek_2021_Interpretable_ML_Satellite_Imagery", "url": "https://arxiv.org/pdf/2108.10744.pdf"},
    {"title": "FLI_2023_Pause_Giant_AI_Experiments_Open_Letter", "url": "https://futureoflife.org/wp-content/uploads/2023/05/FLI_Pause-Giant-AI-Experiments_An-Open-Letter.pdf"},
    {"title": "Baum_2023_AI_Governance_and_Opportunities", "url": "https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2023.1210421/pdf"},
    {"title": "Larosa_2023_Halting_Generative_AI_Climate_Research", "url": "https://www.researchgate.net/publication/371144523_Halting_generative_AI_advancements_may_slow_down_progress_in_climate_research"},

    # Time-Series Forecasting & Reduced-Order Modeling
    {"title": "Moehlis_2004_Low_Dimensional_Model_Turbulent_Shear_Flow", "url": "https://sites.me.ucsb.edu/~moehlis/moehlis_papers/njp4_1_056.pdf"},
    {"title": "Kim_2005_Transition_To_Turbulence_Couette_Flow", "url": "https://sites.me.ucsb.edu/~moehlis/lina_kim_thesis.pdf"},
    {"title": "Srinivasan_2019_Predictions_Turbulent_Shear_Flows_DNN", "url": "https://arxiv.org/pdf/1905.03634"},
    {"title": "Guastoni_2019_Prediction_Wall_Bounded_Turbulence_CNN", "url": "https://arxiv.org/pdf/1912.12969"},
    {"title": "Eivazi_2021_RNN_Time_Series_Forecasting_Chaotic_Flow", "url": "https://arxiv.org/pdf/2005.02762"},
    {"title": "Borrelli_2022_LSTM_Temporal_Dynamics_Turbulent_Channels", "url": "https://arxiv.org/pdf/2203.00974"},
    {"title": "Yousif_2023_Transformer_Synthetic_Inflow_Generator", "url": "https://arxiv.org/pdf/2206.01618"},

    # Physics-Informed Neural Networks (PINNs) & Datasets
    {"title": "Eivazi_2022_PINN_RANS_Navier_Stokes", "url": "https://arxiv.org/pdf/2107.10711"},
    {"title": "EitelAmor_2014_Simulation_Zero_Pressure_Gradient_TBL", "url": "https://torroja.dmt.upm.es/congresos/etc13/Proceedings/PDF/027_ETC13.pdf"},
    {"title": "Bobke_2017_Adverse_Pressure_Gradient_TBL", "url": "https://www.diva-portal.org/smash/get/diva2:919885/FULLTEXT01.pdf"},
    {"title": "Hasanuzzaman_2023_PINN_PIV_Measurements", "url": "https://opus4.kobv.de/opus4-btu/files/6169/Hasanuzzaman_Enhancement.pdf"},
    {"title": "Eivazi_2024_DeNoising_Fluid_Flow_PINN", "url": "https://arxiv.org/pdf/2203.15402"},

    # General AI Milestones
    {"title": "Silver_2016_Mastering_Game_of_Go_AlphaGo", "url": "https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf"},
    {"title": "Silver_2017_Mastering_Go_Without_Human_Knowledge", "url": "https://augmentingcognition.com/assets/Silver2017a.pdf"},

    # Key Literature in ML for Fluid Dynamics
    {"title": "Milano_2002_Neural_Network_Modeling_Turbulent_Flows", "url": "https://cse-lab.seas.harvard.edu/sites/projects.iq.harvard.edu/files/koumoutsakos2025.pdf"},
    {"title": "Beck_2018_DNN_LES_Subgrid_Scale_Modeling", "url": "https://arxiv.org/pdf/1806.04482.pdf"},
    {"title": "Fukami_2019_Super_Resolution_Reconstruction_Turbulent_Flows", "url": "https://arxiv.org/pdf/1811.11328.pdf"},
    {"title": "Duraisamy_2019_Turbulence_Modeling_Age_of_Data", "url": "https://arxiv.org/pdf/1804.00183.pdf"},
    {"title": "Raissi_2020_Hidden_Fluid_Mechanics", "url": "https://arxiv.org/pdf/1808.04327.pdf"},
    {"title": "Brunton_2019_Machine_Learning_for_Fluid_Mechanics", "url": "https://arxiv.org/pdf/1905.11075.pdf"},
    {"title": "Vinuesa_2023_Enhancing_Experimental_Fluid_Mechanics_ML", "url": "https://arxiv.org/pdf/2303.15832.pdf"},

    # Non-Intrusive Sensing, Wall Predictions & Super-Resolution
    {"title": "Suzuki_2017_Linear_Estimation_Turbulent_Channel_Flow", "url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/FF3F666C31E923A90250E18D6EEECA99/S0022112017005808a.pdf"},
    {"title": "Encinar_2018_Logarithmic_Layer_Turbulence", "url": "https://arxiv.org/pdf/1812.01354.pdf"},
    {"title": "Sasaki_2019_Transfer_Functions_Wall_Bounded_Turbulence", "url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/63490EA6024E918C3E978E5A9C841439/S0022112019000272a.pdf/transfer-functions-for-flow-predictions-in-wall-bounded-turbulence.pdf"},
    {"title": "Li_1984_Spatial_Neural_Network_Architectures", "url": "https://s3.amazonaws.com/arena-attachments/2618226/4497a1ae3a5e18d1d9e90a7748c1f9b9.pdf"},
    {"title": "Chevalier_2007_SIMSON_Pseudo_Spectral_Solver", "url": "https://www.mech.kth.se/~mattias/simson-user-guide-v4.0.pdf"},
    {"title": "Guemes_2019_Wall_Measurements_Off_Wall_Velocity_Fields", "url": "https://arxiv.org/pdf/2103.07387.pdf"},
    {"title": "Guastoni_2020_Transfer_Learning_Non_Intrusive_Sensing", "url": "https://arxiv.org/pdf/1912.12969.pdf"},
    {"title": "Guastoni_2021_CNN_Non_Intrusive_Sensing", "url": "https://arxiv.org/pdf/2006.12483.pdf"},
    {"title": "Kim_2021_Unsupervised_GAN_Fluid_Flow_Super_Resolution", "url": "https://arxiv.org/pdf/2007.15324.pdf"},
    {"title": "Guemes_2021_Super_Resolution_GAN_Turbulent_Wall", "url": "https://arxiv.org/pdf/2103.07387.pdf"},
    {"title": "Mizuno_2013_Wall_Bounded_Turbulence_High_Reynolds", "url": "https://torroja.dmt.upm.es/pubs/2013/MizJim_jfm13.pdf"},
    {"title": "Balasubramanian_2023_Near_Wall_Predictions_CNN", "url": "https://arxiv.org/pdf/2303.00706.pdf"},

    # Coherent Structures, Physics Discovery & Explainable AI
    {"title": "LozanoDuran_2012_3D_Intensity_Structures_Turbulent_Channels", "url": "https://torroja.dmt.upm.es/pubs/2012/ald_of_jj_2012_JFM.pdf"},
    {"title": "Lundberg_2017_Kernel_SHAP_NeurIPS", "url": "https://proceedings.neurips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.pdf"},
    {"title": "Lee_2019_Towing_Tank_PIV_Turbulent_Boundary_Layer", "url": "http://www.tsfp-conference.org/proceedings/2019/171.pdf"},
    {"title": "Erion_2021_Gradient_SHAP_Nature_MI", "url": "https://arxiv.org/pdf/1906.10670"},
    {"title": "LozanoDuran_2022_Information_Theoretic_Analysis_Turbulence", "url": "https://arxiv.org/pdf/2111.09484"},
    {"title": "Encinar_2023_Cause_Effect_Streaks_Vortices_JFM", "url": "https://torroja.dmt.upm.es/pubs/2023/EncinarJim_JFM23.pdf"},
    {"title": "Cremades_2024_Key_Coherent_Structures_XAI", "url": "https://core.ac.uk/download/pdf/613862705.pdf"},
    {"title": "Cremades_2025_Point_by_Point_SHAP_Analysis", "url": "https://arxiv.org/pdf/2410.23189"},
]


def sanitize_filename(title: str) -> str:
    """Sanitize a paper title into a safe filename ending in .pdf"""
    # Remove characters that are illegal/unsafe in filenames.
    cleaned = re.sub(r'[\\/:*?"<>|]', "", title)
    # Replace whitespace with underscores and collapse repeats.
    cleaned = re.sub(r"\s+", "_", cleaned.strip())
    cleaned = re.sub(r"_+", "_", cleaned)
    return f"{cleaned}.pdf"


def download_paper(paper: dict, output_dir: str) -> tuple[str, str, str]:
    """Download a single paper. Returns (status, title, detail)."""
    title = paper["title"]
    url = paper["url"]
    filename = sanitize_filename(title)
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        return ("skipped", title, "file already exists")

    try:
        response = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT_SECONDS, stream=True
        )
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return ("downloaded", title, filename)
    except Exception as exc:
        # Remove any partially written file on failure.
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
        return ("failed", title, str(exc))


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = {"downloaded": 0, "skipped": 0, "failed": 0}
    failed_details = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_paper, paper, OUTPUT_DIR): paper
            for paper in papers
        }

        for future in as_completed(futures):
            status, title, detail = future.result()
            results[status] += 1

            if status == "downloaded":
                print(f"[Downloaded] {title} -> {detail}")
            elif status == "skipped":
                print(f"[Skipped] {title} ({detail})")
            else:
                print(f"[Failed] {title}: {detail}")
                failed_details.append((title, detail))

    total = len(papers)
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Total papers:  {total}")
    print(f"Downloaded:    {results['downloaded']}")
    print(f"Skipped:       {results['skipped']}")
    print(f"Failed:        {results['failed']}")

    if failed_details:
        print("\nFailed downloads:")
        for title, detail in failed_details:
            print(f"  - {title}: {detail}")

    sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
