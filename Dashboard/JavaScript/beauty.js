$(document).ready(function() {

  //List of tags
  var beautyTags = ['beauty', 'lipstick', 'makeup', 'make up',
                    'cosmetics', 'fashion'];

  //key: tag, value: freq
  var map = new Map();

  function tagsData( passedCategory ) {
    map.clear();

    for (var element in wordsCat) {
        //console.log(wordsCat[element][1]);
        for (var property in wordsCat[element]) {

            for (var each in wordsCat[element][1]){

              if (passedCategory == wordsCat[element][0]) {

                var key = wordsCat[element][1][each].toLowerCase();

                  if (map.has(key) != true) {
                    //the tag doesnt exist in Map
                    map.set(key, 1);
                  } else {
                    //tag exists in Map
                    var value = map.get(key) + 1;
                    map.set(key, value);
                  }

               } else if (passedCategory == 'All') {
                 var key = wordsCat[element][1][each].toLowerCase();

                   if (map.has(key) != true) {
                     //the tag doesnt exist in Map
                     map.set(key, 1);
                   } else {
                     //tag exists in Map
                     var value = map.get(key) + 1;
                     map.set(key, value);
                   }
			   }//if
            } //for
        } //for
     } //for
  } //End function tagsData(passedCategory)

  var tableData = [];
  var pieCategory = [];
  var pieFreq = []; //Frequency of respective pieCategory
  var totalVids = 0;

  var datalength = 0
  var wordsCat = [];

  //testing
  var testBeautyTag = "";
  var testActualTag = "";

  //Pulls data for the Google charts
  for (var element in jsonDATA) {
    for (var property in jsonDATA[element]) {

      var containsTag = false;

      for (var each in jsonDATA[element][property]['Tags']) {
        var currentTag = jsonDATA[element][property]['Tags'][each].toLowerCase();

        for (var n in beautyTags) {
          if (currentTag.indexOf(beautyTags[n]) > -1) {
            //console.log(currentTag.indexOf(n));
            //console.log (beautyTags[n]);
            containsTag = true;
            testBeautyTag = beautyTags[n];
            testActualTag = currentTag;

            //console.log(jsonDATA[element][property]['Tags']);
          }
        }

      }

      if (containsTag == true) {
        datalength++;
        tableData.push([
                        jsonDATA[element][property]['ChannelName'],
                        Number(jsonDATA[element][property]['SubCount']),
                        jsonDATA[element][property]['Title'],
                        jsonDATA[element][property]['VideoLength'],
                        Number(jsonDATA[element][property]['ViewCount']),
                        jsonDATA[element][property]['Categories']
                      ]);

        wordsCat.push([jsonDATA[element][property]['Categories'], jsonDATA[element][property]['Tags']]);
      //  console.log("Title: " + jsonDATA[element][property]['Title']);
      //  console.log("Tags: " + jsonDATA[element][property]['Tags']);
      //  console.log("Beauty Tag: " + testBeautyTag);
      //  console.log("Actual Tag: " + testActualTag);
        var currentCategory = jsonDATA[element][property]['Categories'];

        //Pushing data into arrays
        if (pieCategory.length < 1) {
          //array is empty
          pieCategory.push(currentCategory);
          pieFreq.push(1);
        } else if (pieCategory.indexOf(currentCategory) == -1) {
          //category element does not exist
          pieCategory.push(currentCategory);
          pieFreq.push(1);
        } else {
        //category element exists in pieCategory array
        pieFreq[pieCategory.indexOf(currentCategory)]++;
        }
      } //if statement containgsTag == true

    }
  } //end double for loop

  //Formats data for Pie Chart
  var pieData = [];
  var totalVids = datalength;
  pieData.push(['Category', 'Percentage']);

  for (var i=0; i < pieCategory.length; i++) {
    pieData.push([ pieCategory[i], (pieFreq[i]/totalVids) ]);
    console.log(pieCategory[i] + " : "+(pieFreq[i]/totalVids) );
  }

  /**
   * Google Charts
   */

  //Load Charts and corechart & barchart packages
  google.charts.load('current', {'packages':['table','corechart', 'controls']});

  //Draw the charts
  google.charts.setOnLoadCallback(drawTable);
  google.charts.setOnLoadCallback(drawPie);

  //Options for Data Table
  var tableOptions = {
                        showRowNumber: true,
                      };

  //Options for Pie Chart
  var pieOptions = { //legend: {position: ''},
                      pieSliceText: 'label',
                      title: 'Video Categories',
                      pieStartAngle: 100,
                      chartArea:{
                        top: 20,
                        width:'90%',
                        height:'90%'
                      },
                      backgroundColor: {
                        stroke: '#00178a',
                        strokeWidth: 3,
                      },
                      colors: ['#e11383', '#ffa400', '#45c1e1', '#eb0029', '#95d600', '#978882',
                               '#3366CC','#DC3912','#109618', '#990099','#3B3EAC','#0099C6',
                               '#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11']
                    };

var csvTableData;
  //Draws Google Table Chart
  function drawTable() {
    var dashboard = new google.visualization.Dashboard(
      document.getElementById('dashboard_div'));

      programmaticSlider = new google.visualization.ControlWrapper({
        'controlType': 'CategoryFilter',
        'containerId': 'control_div',
        'options': {
          'filterColumnLabel': 'Category',
          'ui': {'labelStacking': 'vertical'}
        }
      });

      programmaticChart  = new google.visualization.ChartWrapper({
       'chartType': 'Table',
       'containerId': 'table_div',
       'options': tableOptions
     });

     var data = new google.visualization.DataTable();
     data.addColumn('string', 'Channel Name');
     data.addColumn('number', 'Subscriber Count');
     data.addColumn('string', 'Video Title');
     data.addColumn('string', 'Video Length');
     data.addColumn('number', 'Total Views');
     data.addColumn('string', 'Category');
     //data.addColumn('timeofday', 'Time of Day');

     data.addRows(tableData);

     dashboard.bind(programmaticSlider, programmaticChart);
     dashboard.draw(data);
     csvTableData = data;
  }

  //Draws the Google Pie Chart
  function drawPie() {
    var data = google.visualization.arrayToDataTable(pieData);

    var chart = new google.visualization.PieChart(document.getElementById('pie_div'));
    chart.draw(data, pieOptions);
  }

  /* End Google Charts */

  /**
   * Word Cloud
   */

   var cloudOptions = {
     shape: 'rectangular',
     autoResize: true,
   }

   //add categories to word cloud drop down list
   for (var k=0; k < pieCategory.length; k++) {
     $('#cloudSelect').append($('<option>', {
       value: k,
       text: pieCategory[k]
     }));
   }

   var words = [];
   $( "#cloudSelect" ).change(function() {
     words.length = 0;

     $( "#cloudSelect option:selected" ).each(function() {
       var selectedCategory = $("#cloudSelect option:selected").text();
       tagsData(selectedCategory);

       for (var [key, value] of map) {
         //console.log(key + "=" + value);
         words.push({text: key, weight: value});
       }
     });

    $('#tagwords').empty();
    $("#tagwords").jQCloud(words, cloudOptions);
  })
  .trigger( "change" );

  /* End Word Cloud */

  //Exports Data Table data to enable its download as CSV
  $('#exportTable').click(function () {
      var csvFormattedDataTable = google.visualization.dataTableToCsv(csvTableData);
      //console.log(csvFormattedDataTable);
      var encodedUri = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csvFormattedDataTable);
      this.href = encodedUri;
      this.download = 'table-data.csv';
      this.target = '_blank';
  });

  //Side Navigation Toggle
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

});
