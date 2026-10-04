"""Three practice problems: data structure selection and runtime reasoning."""

from collections import deque
import unittest


def has_duplicates(product_ids):
    """Return whether a collection of hashable product IDs contains a repeat."""
    # A set fits because only membership matters, not order or duplicate counts.
    # Membership checks and insertions take expected O(1) time per ID, giving
    # expected O(n) total time and O(n) space, with an early return on a repeat.
    seen = set()
    for product_id in product_ids:
        if product_id in seen:
            return True
        seen.add(product_id)
    return False


class TaskQueue:
    """Maintain tasks in arrival order; an empty removal raises IndexError."""

    # A deque implements FIFO behavior so the oldest task leaves first.
    # append and popleft each take O(1) time without shifting the remaining
    # tasks, and storing n pending tasks requires O(n) space.
    def __init__(self):
        self._tasks = deque()

    def add_task(self, task):
        self._tasks.append(task)

    def remove_oldest_task(self):
        if not self._tasks:
            raise IndexError("Cannot remove a task from an empty queue")
        return self._tasks.popleft()


class UniqueTracker:
    """Track distinct integers seen so far without retaining duplicates."""

    # A set naturally stores each distinct integer once, making it suitable
    # for a stream whose unique count is needed at any time.
    # Adding a value takes expected O(1) time, len takes O(1), and storage
    # takes O(u) space for u unique values.
    def __init__(self):
        self._values = set()

    def add(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("value must be an integer (not a boolean)")
        self._values.add(value)

    def get_unique_count(self):
        return len(self._values)


class PracticeTests(unittest.TestCase):
    def test_duplicate_examples(self):
        self.assertTrue(has_duplicates([10, 20, 30, 20, 40]))
        self.assertFalse(has_duplicates([1, 2, 3, 4, 5]))

    def test_duplicate_boundaries(self):
        self.assertFalse(has_duplicates([]))
        self.assertFalse(has_duplicates([10]))
        self.assertTrue(has_duplicates([10, 10]))
        self.assertTrue(has_duplicates(["A", "B", "A"]))
        self.assertFalse(has_duplicates(iter([1, 2, 3])))

    def test_duplicate_invalid_inputs(self):
        with self.assertRaises(TypeError):
            has_duplicates(None)
        with self.assertRaises(TypeError):
            has_duplicates([[1], [1]])  # IDs must be hashable.

    def test_queue_fifo_and_reuse(self):
        queue = TaskQueue()
        queue.add_task("Email follow-up")
        queue.add_task("Code review")
        self.assertEqual(queue.remove_oldest_task(), "Email follow-up")
        queue.add_task("Write tests")
        self.assertEqual(queue.remove_oldest_task(), "Code review")
        self.assertEqual(queue.remove_oldest_task(), "Write tests")
        with self.assertRaises(IndexError):
            queue.remove_oldest_task()
        queue.add_task(None)  # Tasks may be arbitrary objects.
        self.assertIsNone(queue.remove_oldest_task())

    def test_queue_independent_instances(self):
        first, second = TaskQueue(), TaskQueue()
        first.add_task("A")
        with self.assertRaises(IndexError):
            second.remove_oldest_task()

    def test_unique_stream(self):
        tracker = UniqueTracker()
        self.assertEqual(tracker.get_unique_count(), 0)
        for value, expected in [(10, 1), (20, 2), (10, 2), (-1, 3), (0, 4)]:
            tracker.add(value)
            self.assertEqual(tracker.get_unique_count(), expected)

    def test_unique_invalid_inputs_do_not_change_state(self):
        tracker = UniqueTracker()
        tracker.add(10)
        for value in ["10", 1.5, None, True, []]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    tracker.add(value)
                self.assertEqual(tracker.get_unique_count(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
