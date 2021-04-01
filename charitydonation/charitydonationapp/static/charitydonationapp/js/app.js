document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
      this.fetching("/institutions-1", ".help--slides-items.in1");
      this.fetching("/institutions-2", ".help--slides-items.in2");
      this.fetching("/institutions-3", ".help--slides-items.in3");
    }

    fetching (link, query_selector) {
      fetch(link, {
          method : "GET",
      }).then( resp => {
          return resp.json();
      }).then( obj => {
          console.log(obj);
          const items = document.querySelectorAll(query_selector);

          items.forEach(itemsTab => {
            itemsTab.innerHTML = '';
            obj.results.forEach(element => {
              let institution = document.createElement("li");
  
              let institution_details = document.createElement("div");
              institution_details.classList.add("col");
              institution.appendChild(institution_details);
  
              let instTitle = document.createElement("div");
              instTitle.classList.add("title");
              instTitle.innerText = element.name;
              institution_details.appendChild(instTitle);
  
              let instSubtitle = document.createElement("div");
              instSubtitle.classList.add("subtitle");
              instSubtitle.innerText = element.description;
              institution_details.appendChild(instSubtitle);

              let institution_categories = document.createElement("div");
              institution_categories.classList.add("col");
              institution.appendChild(institution_categories);
  
              let instText = document.createElement("div");
              instText.classList.add("text");
              let categories = "";
              element.categories.forEach(category => {
                categories += `${category.name} `;
              });
              instText.innerText = categories;
              institution_categories.appendChild(instText);
  
              itemsTab.appendChild(institution);
            });

          });

      });
    };

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          if (e.target.parentElement.parentElement.classList.contains("in1")) {
            this.changePage(e, "1");
          }
          if (e.target.parentElement.parentElement.classList.contains("in2")) {
            this.changePage(e, "2");
          }
          if (e.target.parentElement.parentElement.classList.contains("in3")) {
            this.changePage(e, "3");
          }
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e, type) {
      e.preventDefault();
      const page = e.target.dataset.page;
      const api_url = `/institutions-${type}/?page=${page}`;
      const type_class = `.help--slides-items.in${type}`;

      this.fetching(api_url, type_class);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary

      const checkboxes = document.querySelectorAll(".categoryCheckbox:checked");
      let categories = [];
      checkboxes.forEach((checkbox) => {
          categories.push(checkbox.value);
      });
      let classes = categories.join(".")
      let all_classes = `.${classes}`;

      const institutions = document.querySelectorAll(all_classes).forEach((el) => {
        el.removeAttribute("hidden");
      });

      //final summary
      let bag_amount = 0
      const bag_quantity = document.getElementsByName("bags").forEach((el) => {
        bag_amount += el.value;
      });
      let all_categories = categories.join(", ");
      const summ_categories = document.querySelectorAll("#summ-categories").forEach((el) => {
        el.innerText = `worków: ${bag_amount} z tych kategorii: ${all_categories}`;
      });
      
      let org_name = ""
      const checked_organization = document.querySelectorAll(".organizationCheckbox:checked").forEach((el) => {
        org_name = el.value;
      });
      const summ_organization = document.querySelectorAll("#summ-organization").forEach((el) => {
        el.innerText = `wybrana organizacja: ${org_name}`;
      });

      function infoSummary(input_name, summ_id) {
        let input_value = ""
        const inputs = document.getElementsByName(input_name).forEach((el) => {
          input_value = el.value;
        });
        const summary_id = document.querySelectorAll(`#${summ_id}`).forEach((el) => {
          el.innerText = input_value;
        });
      };

      infoSummary("address", "summ-address");
      infoSummary("city", "summ-city");
      infoSummary("postcode", "summ-postcode");
      infoSummary("phone", "summ-phone");
      infoSummary("data", "summ-data");
      infoSummary("time", "summ-time");
      infoSummary("more_info", "summ-more_info");

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  };

});