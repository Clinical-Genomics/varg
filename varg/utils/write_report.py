from sys import stdout

from .compare import Comparison



class ReportWriter:

    def __init__(self, compare_iter, vcf_fields):

        self.compare_iter =  compare_iter
        self.aggr_stats = StatsHelper()
        self.vcf_fields = vcf_fields

    def write(self):

        for records in self.compare_iter:
            comp = Comparison(records[0], records[1],  vcf_keys=self.vcf_fields, sample_idx_map=records[2])
            self._update_aggr_stats(comp)
            self._write_line(comp)
        self.aggr_stats.compile_stats()
        self.aggr_stats.write_stats()

    @staticmethod
    def _write_line(comp):
        print(comp)

    def _update_aggr_stats(self, comp):

        for key, value in comp.comparison.items():
            self.aggr_stats.push_stats(field_name=key, stats=value[2])


class StatsHelper:

    def __init__(self):
        self.stats = dict()

    def _add_field(self, field_name: str):
        self.stats[field_name] = dict()

    def _get_fields(self):
        return list(self.stats.keys())

    def push_stats(self, field_name: str, stats: dict):
        if field_name not in self._get_fields():
            self._add_field(field_name)
            self.stats[field_name]['comparisons'] = 0
        for key, value in stats.items():
            if key == 'status':
                if value not in self.stats[field_name].keys():
                    self.stats[field_name][value] = 1
                else:
                    self.stats[field_name][value] += 1
            elif key == 'diff':
                if 'acc_diff' not in self.stats[field_name].keys():
                    self.stats[field_name]['acc_diff'] = value
                else:
                    self.stats[field_name]['acc_diff'] += value
        self.stats[field_name]['comparisons'] += 1

    def compile_stats(self):

        for key, value in self.stats.items():
            if value.get('acc_diff') is not None:
                acc_diff = self.stats[key].pop('acc_diff')
                self.stats[key]['mean_diff'] = acc_diff / self.stats[key]['comparisons']

    def write_stats(self):
        print(str(self))

    def __str__(self):
        stats_str = ""
        for field_name, field_value in self.stats.items():
            stats_str += '\n' + field_name
            for key, value in field_value.items():
                stats_str += '\n\t' + key + ': ' + str(value)
        return stats_str

    def __dict__(self):
        return self.stats
