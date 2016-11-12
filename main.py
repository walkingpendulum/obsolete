import sys
import time


class iterate_with_ETA_output(object):
    """
    usage:
    >> iterable = [x for x in range(10**6)]
    >> for x in iterate_with_ETA_output(iterable):
           pass

    """

    @staticmethod
    def _gen(iterable):
        for ind, value in enumerate(iterable):
            yield ind, value

    def __init__(self, iterable, total=None, stream=None):
        if not total:
            if not hasattr(iterable, '__len__'):
                raise NotImplementedError("Iterable has no __len__, specify 'total' argument")
            total = len(iterable)
        self.total = total
        self.start_time = int(time.time())
        self.iterator = self._gen(iterable)
        if isinstance(stream, str):
            self.stream = open(stream, 'w')
        self.stream = stream if stream else sys.stdout
        self.not_stdout = bool(stream)

    def print_to_stream(self, msg):
        print(msg, end='', file=self.stream, flush=True)

    def close_stream_if_needed(self):
        if self.not_stdout:
            self.stream.close()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            ind, value = next(self.iterator)
            rate = (1 + ind) / self.total
            percentage = 100 * rate

            _passed_seconds = time.time() - self.start_time
            passed_seconds = int(_passed_seconds)
            passed_m, passed_s = divmod(passed_seconds, 60)

            eta_seconds = int(_passed_seconds * ((1 - rate) / rate))
            eta_m, eta_s = divmod(eta_seconds, 60)

            _total_seconds = _passed_seconds / rate
            total_seconds = int(_total_seconds)
            total_m, total_s = divmod(total_seconds, 60)

            str_template = "%02d:%02ds"
            passed_str = str_template % (passed_m, passed_s)
            eta_str = str_template % (eta_m, eta_s)
            total_str = str_template % (total_m, total_s)

            _output_str = '{:.2f}%, ETA {}, passed {}, total ~ {}'.format(percentage, eta_str, passed_str, total_str)
            output_str = '\r' + '{:<60}'.format(_output_str)

            self.print_to_stream(output_str)
            return value
        except StopIteration:
            self.print_to_stream('\n')  # перевод строки
            self.close_stream_if_needed()
            raise
        except KeyboardInterrupt:
            self.print_to_stream('\n')  # перевод строки
            self.close_stream_if_needed()
            raise StopIteration
