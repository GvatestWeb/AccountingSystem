$(function () {

  var currentActive = "#goods",
      butAdd = $(".button-add"),
      form = $(".form"),
      cancel = $(".cancel"),
      submit = $(".submit")

  if ($("tbody").children().text() == "") {
    $(".button-start").css({"display": "block"})
    data = eel.nomencl_output()()
    data.then(getData, error => {console.log("can't get resp from goods")})
  }

  // Get Data From table
  async function getData(goods) {
    datadb = "<tr class='titles'>"
    for (var i = 0; i < goods["titles"].length; i++) {
      datadb += `<td data="${goods['titles'][i]}">${goods['titles'][i][0]}</td>`
    }
    for (var i = 0; i < goods["values"].length; i++) {
      datadb += "<tr>"
      for (var j = 0; j < goods['values'][i].length; j++) {

        datadb += `<td class="${goods['titles'][j][0]}">${goods['values'][i][j]}</td>`
      }
      datadb += "</tr>"
    }
    $("tbody").append(datadb)
  }

  $(".button-start").on('click', async function () {
    $(".form-expl").css({"display": "block"})
  })

  $(".button-update").on('click', async function () {
    $(".form-body_update").empty()
    select = `<div class="row"><label>Type Of Names</label><select class="type_input"><option disabled>Выберете тип номенклатуры</option>`
    statuses = eel.names_for_change()()
    statuses = await statuses.then(statuses => {return statuses}, error => {console.log("can't get response from Type Of Names table")})
    statuses.forEach(element => {
      select += `<option value="${element}">${element}</option>`
    });
    select += "</select></div>"
    price_input = '<div class="row"><label for="">New Price</label><input type="text" placeholder="New Price" class="input price_input"></div>'
    $(".form-body_update").append(select)
    $(".form-body_update").append(price_input)
    $(".form-update").css({"display": "block"})
  })

  $(".submit_update").on('click', async function () {
    if ($(".type_input").val() && !isNaN($(".price_input").val())) {
      $("tbody").empty()
      await eel.change_of_price($(".type_input").val(), $(".price_input").val())
      data = eel.prices_output()()
      data.then(getData, error => {console.log("can't get resp from prices table")})
    } else {
      alert("Incorrect input")
    }
    $(".form-update").css({"display": "none"})
  })

  $(".cancel_update").on('click', async function () {
    $(".form-update").css({"display": "none"})
  })

  // Open Add Form
  butAdd.on('click', async function () {
    if (currentActive == "#payment") {
      // User ID
      $(".form-body_pay").empty()
      select = `<div class="row"><label>User ID</label><select><option disabled>Выберете user Id</option>`
      users_id = eel.users_list()()
      users_id = await users_id.then(users_id => {return users_id}, error => {console.log("can't get response from users table")})
      users_id.forEach(element => {
        select += `<option value="${element}">${element}</option>`
      });
      select += "</select></div>"
      $(".form-body_pay").append(select)

      // Article
      select = `<div class="row"><label>Articul</label><select><option disabled>Выберете артикул</option>`
      users_id = eel.products_list()()
      users_id = await users_id.then(users_id => {return users_id}, error => {console.log("can't get response from nomencl table")})
      users_id.forEach(element => {
        select += `<option value="${element}">${element}</option>`
      });
      select += "</select></div>"
      $(".form-body_pay").append(select)
      select = '<div class="row"><label for="${data[0]}">Date of start</label><input id="date_of_start" type="text" placeholder="1:21 1:12:2021"></div>'
      $(".form-body_pay").append(select)
      $(".form-pay").css({"display": "block"})
    } else {
      titles = $(".titles").children()
      for (var i = 0; i < titles.length; i++) {
        title = titles[i]
      }
      $(".form-body").empty()
      for (var i = 0; i < titles.length; i++) {
        text = titles[i].innerHTML
        data = $(titles[i]).attr("data").split(",")
        if (data[3] == "tel") {
          $(".form-body").append(`<div class="row"><label for="${data[0]}">${data[0]}</label><input id="${data[0]}" type="${data[3]}" maxlength="${data[2]}" type="text" placeholder="+999(999)123-12-12"></div>`)
        } else if (data[3] == "select" && currentActive == "#users") {
          select = `<div class="row"><label>${data[0]}</label><select><option disabled>Выберете статус</option>`
          statuses = eel.statuses_output()()
          statuses = await statuses.then(statuses => {return statuses}, error => {console.log("can't get response from statuses table")})
          statuses.forEach(element => {
            select += `<option value="${element[1]}">${element[1]}</option>`
          });
          select += "</select></div>"
          $(".form-body").append(select)
        } else if (data[3] == "select" && (currentActive == "#goods" | currentActive == "#prices")) {
          select = `<div class="row"><label>${data[0]}</label><select><option disabled>Выберете тип номенклатуры</option>`
          statuses = eel.names_for_change()()
          statuses = await statuses.then(statuses => {return statuses}, error => {console.log("can't get response from type_of_names table")})
          statuses.forEach(element => {
            select += `<option value="${element}">${element}</option>`
          });
          select += "</select></div>"
          $(".form-body").append(select)
        } else if (data[3] == "hidden") {
        } else $(".form-body").append(`<div class="row"><label for="${data[0]}">${data[0]}</label><input id="${data[0]}" type="${data[3]}" maxlength="${data[2]}" type="text" placeholder="${text}"></div>`)
      }
      form.css({'display':'block'})
    }
  })

  // Cancel 
  cancel.on('click', function () {
    form.css({'display':'none'})
  })


  $(".cancel_pay").on('click', function () {
    $(".form-pay").css({'display':'none'})
  })

  $(".submit_pay").on('click', async function () {
    formBody = $(".form-body_pay").children()
    values_update = []
    for (var i = 0; i < formBody.length; i++) {
      row = formBody[i]
      input = $(row).children()[1]
      values_update.push($(input).val())
    }
    flag = 1
    for (var i = 0; i < values_update.length; i++) {
      if (!values_update[i]) {
        flag = 0
        break
      }
    }
    if (flag == 1) {
      payment = eel.payment(values_update[0], values_update[1], values_update[2])()
      payment = await payment.then(payment => {return payment}, error => {console.log("can't get response from payment table")})
    }
    $(".form-pay").css({'display':'none'})
  })

  // Add 
  submit.on('click', async function () {
    var formData = "<tr>"
    values_update = []
    formBody = $(".form-body").children()
    for (var i = 0; i < formBody.length; i++) {
        if (i == 4 && $('input:checkbox:checked').val() && currentActive == "#goods") {
          formData += "<td>Yes</td>"
          values_update.push("Yes")
        } else if (i == 4 && currentActive == "#goods") {
          row = formBody[i]
          input = $(row).children('input')
          formData += "<td>No</td>"
          values_update.push("No")
        } else {
          row = formBody[i]
          input = $(row).children()[1]
          formData += "<td>" + $(input).val() + "</td>"
          values_update.push($(input).val())
      }
    }
    flag = 1
    for (var i = 0; i < values_update.length; i++) {
      if (!values_update[i]) {
        flag = 0
        break
      }
    }
    if (flag == 1) {
      if (currentActive != "#prices") {
        $("tbody").append(formData + "</tr>")
      }
      if (currentActive == "#goods") {
        await eel.nomencl_append(values_update)
      } else if (currentActive == "#stations") {
        await eel.stations_append(values_update)
      } else if (currentActive == "#users") {
        await eel.users_append(values_update)
      } else if (currentActive == "#prices") {
        $("tbody").empty()
        await eel.prices_append(values_update)
        data = eel.prices_output()()
        await data.then(getData, error => {alert("Can't get response from prices table")})
      }
      form.css({'display':'none'})
    } else alert("Incorrect Input")
  })

  // Open delete form
  $(".button-delete").on('click', function () {
    $(".form-delete").css({'display':'block'})
  })

  // Delete
  $(".submit_delete").on("click", async function () {
    $(".form-delete").css({'display':'none'})
    $("tbody").empty()
    if (!isNaN($(".delete_input").val())) {
      if (currentActive == "#goods") {
        await eel.nomencl_delete($(".delete_input").val())
        data = eel.nomencl_output()()
      } else if (currentActive == "#stations") {
        await eel.stations_delete($(".delete_input").val())
        data = eel.stations_output()()
      } else if (currentActive == "#users") {
        await eel.users_delete($(".delete_input").val())
        data = eel.users_output()()
      } else if (currentActive == "#prices") {
        await eel.prices_delete($(".delete_input").val())
        data = eel.prices_output()()
      }
      data.then(getData, error => {console.log("can't get resp from goods")})
    } else {
      alert("id must be integer")
    }
  })


  // Cancel Delete
  $(".cancel-delete").on('click', function () {
    $(".form-delete").css({'display':'none'})
  })

  // Nomenclature
    // active element db request
    $("#goods").on('click', async function () {
      $(".table").css({"display": "block"})
      $(".button-start").css({"display": "block"})
      $(".button-update").css({"display": "none"})
      $(".button-add").css({"display": "block"})
      $(".button-delete").css({"display": "block"})
      if (currentActive != "#goods") {
        $(".tab").text($("#goods").text())
      $("tbody").empty()
      $(currentActive).removeClass("active")
      $("#goods").addClass("active")
      currentActive = "#goods"
      data = eel.nomencl_output()()
      await data.then(getData, error => {alert("Can't get response from nomenclature table")})
      }
    })
  
    $(".submit_expl").on('click', async function () {
      if (!isNaN($(".expl_input").val())) {
        $("tbody").empty()
        eel.end_expl($(".expl_input").val())
        data = eel.nomencl_output()()
        data.then(getData, error => {console.log("can't get resp from nomenclature table")})
      } else {
        alert("id must be integer")
      }
      $(".form-expl").css({"display": "none"})
    })
  
    $(".cancel_expl").on('click', async function () {
      $(".form-expl").css({"display": "none"})
    })

  // STATIONS
    // active element db request
    $("#stations").on('click', async function () {
      $(".table").css({"display": "block"})
      $(".button-start").css({"display": "none"})
      $(".button-update").css({"display": "none"})
      $(".button-add").css({"display": "block"})
      $(".button-delete").css({"display": "block"})
      if (currentActive != "#stations") {
        $(".tab").text($("#stations").text())
        $("tbody").empty()
        $(currentActive).removeClass("active")
        $("#stations").addClass("active")
        currentActive = "#stations"
        data = eel.stations_output()()
        await data.then(getData, error => {alert("Can't get response from stations table")})
      }
    })

  // Users
    // active element db request
    $("#users").on('click', async function () {
      $(".table").css({"display": "block"})
      $(".button-start").css({"display": "none"})
      $(".button-update").css({"display": "none"})
      $(".button-add").css({"display": "block"})
      $(".button-delete").css({"display": "block"})
      if (currentActive != "#users") {
        $(".tab").text($("#users").text())
        $("tbody").empty()
        $(currentActive).removeClass("active")
        $("#users").addClass("active")
        currentActive = "#users"
        data = eel.users_output()()
        await data.then(getData, error => {alert("Can't get response from users table")})
      }
    })
  

  // Prices
    // active element db request
    $("#prices").on('click', async function () {
      $(".table").css({"display": "block"})
      $(".button-start").css({"display": "none"})
      $(".button-update").css({"display": "block"})
      $(".button-add").css({"display": "block"})
      $(".button-delete").css({"display": "block"})
      if (currentActive != "#prices") {
        $(".tab").text($("#prices").text())
        $("tbody").empty()
        $(currentActive).removeClass("active")
        $("#prices").addClass("active")
        currentActive = "#prices"
        data = eel.prices_output()()
        await data.then(getData, error => {alert("Can't get response from prices table")})
      }
    })
  
    eel.expose(alert_prices); // Expose this function to Python
      function alert_prices() {
        alert("Price can be changed only one time per day");
      }

  // Story
    // active element db request
    $("#story").on('click', async function () {
      $(".table").css({"display": "block"})
      $(".button-start").css({"display": "none"})
      $(".button-update").css({"display": "none"})
      $(".button-add").css({"display": "none"})
      $(".button-delete").css({"display": "none"})
      if (currentActive != "#story") {
        $(".tab").text($("#story").text())
        $("tbody").empty()
        $(currentActive).removeClass("active")
        $("#story").addClass("active")
        currentActive = "#story"
        data = eel.changes_output()()
        await data.then(getData, error => {alert("Can't get response from story of changes table")})
      }
    })
  
  // Story
    // active element db request
    $("#payment").on('click', async function () {
      $(".button-start").css({"display": "none"})
      $(".button-update").css({"display": "none"})
      $(".button-add").css({"display": "block"})
      $(".button-delete").css({"display": "none"})
      $(".table").css({"display": "none"})
      if (currentActive != "#payment") {
        $(".tab").text($("#payment").text())
        $("tbody").empty()
        $(currentActive).removeClass("active")
        $("#payment").addClass("active")
        currentActive = "#payment"
      }
    })
})