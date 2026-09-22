import pathlib
import unittest


SOURCE = pathlib.Path(__file__).parents[1].joinpath("index.html").read_text()


class PlannedWarningValidation(unittest.TestCase):
    def test_warning_logic_has_thresholds_and_mileage_fallback(self):
        self.assertIn("PLANNED_WARNING_MILEAGE=5000", SOURCE)
        self.assertIn("PLANNED_WARNING_DAYS=30", SOURCE)
        self.assertIn("if(Number.isFinite(currentMileage)&&currentMileage>=0)return currentMileage;", SOURCE)
        self.assertIn("return done.length?Math.max.apply(null,done.map(function(e){return e.mileage;})):null;", SOURCE)
        self.assertIn("Number(e.mileage)<=km+PLANNED_WARNING_MILEAGE", SOURCE)
        self.assertIn("due<=limit", SOURCE)

    def test_warning_is_visible_in_planned_markup(self):
        self.assertIn("#plannedList li.planned-warning", SOURCE)
        self.assertIn("planned-warning-badge", SOURCE)
        self.assertIn("warningReasons=plannedWarning(e,todayDate)", SOURCE)


if __name__ == "__main__":
    unittest.main()
