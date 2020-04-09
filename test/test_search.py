from unittest import TestCase

from tqdm import trange

from graphtage.search import IterativeTighteningSearch
from .test_bounds import RandomDecreasingRange


class TestIterativeTighteningSearch(TestCase):
    def test_iterative_tightening_search(self):
        speedups = 0
        tests = 0
        try:
            t = trange(1000)
            for test_num in t:
                ranges = [RandomDecreasingRange() for _ in range(100)]
                best_range: RandomDecreasingRange = None
                for r in ranges:
                    if best_range is None or r.final_value < best_range.final_value:
                        best_range = r
                search = IterativeTighteningSearch(iter(ranges))
                # with tqdm(desc=str(search.bounds()), leave=False) as substatus:
                #     while search.tighten_bounds():
                #         substatus.total = search.bounds().upper_bound - search.bounds().lower_bound
                #         substatus.desc = f"Test {test_num}: {search.bounds()!s}"
                #         substatus.update(substatus.total - (search.bounds().upper_bound - search.bounds().lower_bound))
                #     substatus.clear()
                while search.tighten_bounds():
                    pass
                result = search.best_match
                tightenings = sum(r.tightenings for r in ranges)
                untightened = 0
                for r in ranges:
                    t_before = r.tightenings
                    while r.tighten_bounds():
                        pass
                    untightened += r.tightenings - t_before
                t.desc = f"{(untightened + tightenings) / tightenings:.01f}x Speedup"
                speedups += (untightened + tightenings) / tightenings
                tests += 1
                self.assertEqual(best_range.final_value, result.final_value)
        finally:
            print(f"Average speedup: {speedups / tests:.01f}x")
