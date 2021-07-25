"""
Generate a report aggregating the preprocessing and evoked plots for all subjects
"""
from mne.report import Report
from src.config.config import get_plots_path


class SubjectReport:

    def __init__(self):
        self.figures = {}

    def add_subject_figures(self, name, figures):
        self.figures[name] = figures

    def generate_report(self):
        report = Report()
        for name, fig_dict in self.figures.items():
            for fig_name, fig in fig_dict.items():
                report.add_figs_to_section(fig, section=name, captions=fig_name)
        report.save(get_plots_path().joinpath('preprocessing_report.html'), open_browser=False, overwrite=True)
