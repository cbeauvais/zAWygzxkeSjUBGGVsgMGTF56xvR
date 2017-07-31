class QuotaConverter:
    @classmethod
    def from_aqu(cls, filename):
        quotas = {}
        with open(filename) as aqu:
            for line in aqu:
                words = line.split()
                if words[0] == '#' and words[2] == '=':
                    name = words[1]
                    val = int(words[3])
                    quotas[name] = {'name': name, 'current': val, 'target': 0, 'total': val}
                elif len(words) == 3 and words[1] == '=':
                    if words[0].endswith('.t'):
                        name = words[0][:-2]
                        if name not in quotas:
                            quotas[name] = {'name': name, 'current': 0, 'target': 0, 'total': 0}
                        quotas[name]['target'] = int(words[2])
                    elif words[0].endswith('.r'):
                        name = words[0][:-2]
                        if name not in quotas:
                            quotas[name] = {'name': name, 'current': 0, 'target': 0, 'total': 0}
                        quotas[name]['current'] = int(words[2])
                    else:
                        name = words[0]
                        if name not in quotas:
                            quotas[name] = {'name': name, 'current': 0, 'target': 0, 'total': 0}
                        quotas[name]['total'] = int(words[2])
        return list(quotas.values())
