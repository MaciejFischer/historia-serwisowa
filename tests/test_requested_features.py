import pathlib
import unittest


SOURCE = pathlib.Path(__file__).parents[1].joinpath("index.html").read_text()


class RequestedFeatureValidation(unittest.TestCase):
    def test_vehicle_identification_and_service_picker_search(self):
        self.assertIn('id="vehicleVin">VIN: <span>VSSZZZ5FZHR047444</span>', SOURCE)
        self.assertIn('id="mPickSearch"', SOURCE)
        self.assertIn("normalizedSearchText(e.title+' '+e.category)", SOURCE)
        self.assertIn("normalizedSearchText(t.label+' '+t.category)", SOURCE)

    def test_optional_reminder_creates_planned_mileage_or_date_entry(self):
        self.assertIn('id="mReminder"', SOURCE)
        self.assertIn('id="mReminderType"', SOURCE)
        self.assertIn("reminder={mileage:mileage+interval,date:null", SOURCE)
        self.assertIn("date:addMonthsToDate(e.date,amount*multiplier)", SOURCE)
        self.assertIn("entries.push(planned);order.push(planned.id);", SOURCE)

    def test_mileage_inputs_are_grouped_without_changing_numeric_storage(self):
        self.assertIn("function fmtMileageInput(value)", SOURCE)
        self.assertIn("function parseMileageInput(value)", SOURCE)
        self.assertIn('class="mileage-input"', SOURCE)
        self.assertIn("mileage:mileage,", SOURCE)

    def test_service_place_is_optional_compatible_and_explicitly_backfilled(self):
        self.assertIn('id="mServicePlace" list="servicePlaceSuggestions"', SOURCE)
        for place in ("EK Racing", "EK Racing Gdańsk", "Maran", "Carsed", "TGE Auto"):
            self.assertIn('value="'+place+'"', SOURCE)
        self.assertIn("backfillSeedServicePlaces();", SOURCE)
        self.assertIn("if(Object.prototype.hasOwnProperty.call(e,'servicePlace'))", SOURCE)
        self.assertIn("normalizedEntry.servicePlace=e.servicePlace==null?null:e.servicePlace.trim()||null", SOURCE)
        self.assertIn("if(e.servicePlace)L.push('   Miejsce / warsztat: '+e.servicePlace);", SOURCE)

    def test_history_can_be_filtered_by_multiple_service_places(self):
        self.assertIn('id="placeBtn">Miejsce', SOURCE)
        self.assertIn('id="placeMenu"', SOURCE)
        self.assertIn('id="placeChips"', SOURCE)
        self.assertIn("selPlaces.indexOf(e.servicePlace||'')<0", SOURCE)
        self.assertIn("data-place=", SOURCE)
        self.assertIn("selPlaces=[];renderCats();renderPlaces();renderTable();renderTop();", SOURCE)

    def test_category_filter_supports_live_accent_insensitive_search(self):
        self.assertIn('id="catSearch" type="search"', SOURCE)
        self.assertIn("normalizedSearchText($('catSearch')?$('catSearch').value:'')", SOURCE)
        self.assertIn("if(e.target.id!=='catSearch')return;", SOURCE)
        self.assertIn("normalizedSearchText(category).indexOf(query)<0", SOURCE)

    def test_planned_list_hides_only_trailing_planned_suffix(self):
        self.assertIn("function plannedDisplayTitle(title){return String(title||'').replace(/\\s*\\(planowana\\)\\s*$/i,'');}", SOURCE)
        self.assertIn("esc(plannedDisplayTitle(e.title))", SOURCE)


if __name__ == "__main__":
    unittest.main()
