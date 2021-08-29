import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class MyTestCase(unittest.TestCase):
    chrome_options = None
    driver = None
    action_chains = None

    @classmethod
    def setUpClass(cls):
        cls.chrome_options = Options()
        cls.chrome_options.add_argument("--disable-extensions")
        cls.chrome_options.add_argument("--incognito")
        cls.chrome_options.add_argument("--disable-popup-blocking")
        cls.chrome_options.add_argument("--start-maximized")

    def setUp(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("https://todomvc.com/examples/angularjs/#/")
        self.driver.implicitly_wait(10)
        self.action_chains = ActionChains(self.driver)

    def get_all_task(self):
        return [t.text for t in self.driver.find_elements_by_xpath("/html/body/ng-view/section/section/ul/li/div")]

    def fill_the_todo_list(self):
        time.sleep(1)
        self.add_a_new_task("Nothing to do")
        self.add_a_new_task("i actually cen do something")
        self.add_a_new_task("Wake up")
        self.add_a_new_task("Clean the house")
        self.add_a_new_task("i'm done")
        time.sleep(1)

    def add_a_new_task(self, task):
        self.driver.find_element_by_xpath("/html/body/ng-view/section/header/form/input").send_keys(task + "\n")

    def edit_a_task(self, task_to_edit, new_task):
        todo_list = self.driver.find_elements_by_xpath("/html/body/ng-view/section/section/ul/li")
        form_list = self.driver.find_elements_by_class_name("edit")
        i = 0
        for i in range(len(todo_list)):
            if todo_list[i].text == task_to_edit:
                print(str(i))
                task_to_edit_line = todo_list[i]
                self.action_chains.double_click(task_to_edit_line).perform()
                for j in range(len(task_to_edit)):
                    form_list[i].send_keys("\u0008")
                form_list[i].send_keys(new_task + "\n")
                break
        return i

    def delete_a_task(self, task_to_delete):
        todo_list = self.driver.find_elements_by_xpath("/html/body/ng-view/section/section/ul/li")
        destroy_elements = self.driver.find_elements_by_class_name("destroy")
        for i in range(len(todo_list)):
            if todo_list[i].text == task_to_delete:
                destroy_element = destroy_elements[i]
                self.action_chains.move_to_element(todo_list[i]).perform()
                destroy_element.click()
                break

    def mark_task_as_completed(self, task_to_mark):
        todo_list = self.driver.find_elements_by_xpath("/html/body/ng-view/section/section/ul/li")
        is_completed_list = self.driver.find_elements_by_class_name("toggle")
        i = 0
        for i in range(len(todo_list)):
            if todo_list[i].text == task_to_mark:
                is_completed_list[i].click()
                time.sleep(1)
                break
        return i

    def mark_completed_task_as_active(self, task_to_mark):
        todo_list = self.driver.find_elements_by_xpath("/html/body/ng-view/section/section/ul/li")
        is_completed_list = self.driver.find_elements_by_class_name("toggle")
        i = 0
        for i in range(len(todo_list)):
            if todo_list[i].text == task_to_mark:
                if is_completed_list[i].is_selected():
                    is_completed_list[i].click()
                break
        time.sleep(1)

    def clear_completed_tasks(self):
        self.driver.find_element_by_class_name("clear-completed").click()
        time.sleep(1)

    def view_all(self):
        self.driver.find_element_by_xpath('/html/body/ng-view/section/footer/ul/li[1]').click()
        time.sleep(1)

    def view_active(self):
        self.driver.find_element_by_xpath('/html/body/ng-view/section/footer/ul/li[2]').click()
        time.sleep(1)

    def view_completed(self):
        self.driver.find_element_by_xpath('//html/body/ng-view/section/footer/ul/li[3]').click()

    def test_add_a_new_task(self):
        time.sleep(1)
        self.add_a_new_task("Clean my house")
        all_task_texts = self.get_all_task()
        self.assertTrue("Clean my house" in all_task_texts, "Clean my house is not in the todo list")

    def test_edit_a_task(self):
        self.fill_the_todo_list()
        task_number = self.edit_a_task("Wake up", "Go to sleep")
        all_task = self.get_all_task()
        print(all_task)
        print(str(task_number))
        self.assertTrue(all_task[task_number] == "Go to sleep", "Go to sleep is not in the todo list")

    def test_delete_a_task(self):
        self.fill_the_todo_list()
        self.delete_a_task("Wake up")
        all_task_texts = self.get_all_task()
        print(all_task_texts)
        self.assertTrue("Wake up" not in all_task_texts, "Wake up still exists")

    def test_mark_task_as_completed(self):
        self.fill_the_todo_list()
        task_number = self.mark_task_as_completed("Wake up")
        self.assertTrue(self.driver.find_elements_by_class_name("toggle")[task_number].is_selected(),
                        "Wake up is not marked as completed")

    def test_mark_completed_task_as_active(self):
        self.fill_the_todo_list()
        task_number = self.mark_task_as_completed("Wake up")
        self.mark_completed_task_as_active("Wake up")
        self.assertFalse(self.driver.find_elements_by_class_name("toggle")[task_number].is_selected(),
                         "Wake up is still marked as completed")

    def test_clear_completed_tasks(self):
        self.fill_the_todo_list()
        self.mark_task_as_completed("Clean the house")
        self.clear_completed_tasks()
        all_task = self.get_all_task()
        self.assertTrue("Clean the house" not in all_task, "completed tasks still in the list")

    def test_view_all(self):
        self.fill_the_todo_list()
        tasks_before_marked = self.get_all_task()
        self.mark_task_as_completed("Clean the house")
        self.view_active()
        self.view_all()
        tasks_after_marked = self.get_all_task()
        self.assertEqual(tasks_before_marked, tasks_after_marked, "Do not see all the tasks")

    def test_view_active(self):
        self.fill_the_todo_list()
        self.mark_task_as_completed("Clean the house")
        self.view_active()
        all_tasks = self.get_all_task()
        self.assertTrue("Wake up" in all_tasks, "Wake up accidentally deleted")
        self.assertTrue("Clean the house" not in all_tasks, "Completed tasks can be seen")

    def test_view_completed(self):
        self.fill_the_todo_list()
        self.mark_task_as_completed("Clean the house")
        self.view_completed()
        all_tasks = self.get_all_task()
        self.assertTrue("Wake up" not in all_tasks, "Active tasks can be seen")
        self.assertTrue("Clean the house" in all_tasks, "Clean the house accidentally deleted")

    def tearDown(self):
        time.sleep(1)
        self.driver.close()




if __name__ == '__main__':
    unittest.main()

