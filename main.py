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
        self.start_time = time.time()
        self.iterator = self._gen(iterable)
        self.stream = stream if stream else sys.stdout
        self.need_to_close = bool(stream)

        time.sleep(1e-3)

    def print_to_stream(self, msg):
        self.stream.write(msg)
        self.stream.flush()

    def close_stream_if_needed(self):
        if self.need_to_close:
            self.stream.close()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            ind, value = next(self.iterator)
            rate = (1 + ind) / self.total
            percentage = 100 * rate

            passed_seconds = int(time.time() - self.start_time)
            passed_m, passed_s = divmod(passed_seconds, 60)
            eta_seconds = int(passed_seconds * ((1 - rate) / rate))
            eta_m, eta_s = divmod(eta_seconds, 60)

            passed_str = "%02d:%02ds" % (passed_m, passed_s)
            eta_str = "%02d:%02ds" % (eta_m, eta_s)
            _output_str = '{:.2f}%, ETA {}, passed {}'.format(percentage, eta_str, passed_str)
            output_str = '\r' + '{:<90}'.format(_output_str)

            self.print_to_stream(output_str)
            return value
        except (StopIteration, KeyboardInterrupt):
            self.print_to_stream('\n')  # перевод строки
            self.close_stream_if_needed()
            raise
