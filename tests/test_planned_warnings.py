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

    def test_warning_refreshes_after_mileage_and_at_day_boundary(self):
        self.assertIn("currentMileage=value;\n  lastChanged=changedAt;\n  renderTop();\n  renderPlanned();", SOURCE)
        self.assertIn("function schedulePlannedWarningRefresh()", SOURCE)
        self.assertIn("clearTimeout(plannedWarningRefreshT);", SOURCE)
        self.assertIn("nextDay.setHours(24,0,0,1000);", SOURCE)
        self.assertIn("renderPlanned();\n    schedulePlannedWarningRefresh();", SOURCE)
        self.assertIn("applyTheme();renderAll();schedulePlannedWarningRefresh();", SOURCE)

    def test_current_mileage_has_accessible_formatted_display(self):
        self.assertIn("function fmtCurrentMileage(m){return m==null?'\\u2014':m.toLocaleString('pl-PL')+' km';}", SOURCE)
        self.assertIn('class="current-km-wrap"', SOURCE)
        self.assertIn('class="current-km-display" id="currentMileageDisplay" aria-live="polite"', SOURCE)
        self.assertIn("fmtCurrentMileage(currentMileage)", SOURCE)
        self.assertIn('aria-label="Edytuj aktualny przebieg w kilometrach"', SOURCE)


if __name__ == "__main__":
    unittest.main()
