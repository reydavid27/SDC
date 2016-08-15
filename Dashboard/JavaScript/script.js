$(document).ready(function() {
  /**
   * Data Preparation
   */

  // Keeps track of tag words and its frequency
  var map = new Map(); //key: tag, value: freq

  //Filters tag data for word cloud based on Category
  function tagsData( passedCategory ) {
    map.clear();

    for (var element in jsonDATA) {
      for (var property in jsonDATA[element]) {
        //If the Category is what you want and it has tags; otherwise skip
        if ( jsonDATA[element][property]['Categories'] == passedCategory
             && jsonDATA[element][property]['Tags'] != null) {
            //For each individual tag
          for (var each in jsonDATA[element][property]['Tags']) {

            var key = jsonDATA[element][property]['Tags'][each].toLowerCase();

            if (map.has(key) != true) {
                //the tag doesnt exist in Map
              map.set(key, 1);
            } else {
                //tag exists in Map
              var value = map.get(key) + 1;
              map.set(key, value);
            }
          }//end for loop

        } // end if statement

      }
    }
  } // end function tagsData

  var tableData = [];
  var pieCategory = [];
  var pieFreq = []; //Frequency of respective pieCategory

  //Pulls data for the Google charts
  for (var element in jsonDATA) {
    for (var property in jsonDATA[element]) {

      tableData.push([
                      jsonDATA[element][property]['ChannelName'],
                      Number(jsonDATA[element][property]['SubCount']),
                      jsonDATA[element][property]['Title'],
                      jsonDATA[element][property]['VideoLength'],
                      Number(jsonDATA[element][property]['ViewCount']),
                      jsonDATA[element][property]['Categories']
                    ]);

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

    }
  }

  //Formats data for Pie Chart
  var pieData = [];
  var totalVids = jsonDATA.length;
  pieData.push(['Category', 'Percentage']);

  for (var i=0; i < pieCategory.length; i++) {
    pieData.push([ pieCategory[i], (pieFreq[i]/totalVids) ]);
    //console.log(pieCategory[i] + " : "+(pieFreq[i]/totalVids) );
  }

  //Formats data for Bar Chart
  var barChart = [];
  barChart.push(  ['Sunday', Number(jsonDAY[0]['Sunday'])],
                  ['Monday', Number(jsonDAY[0]['Monday'])],
                  ['Tuesday', Number(jsonDAY[0]['Tuesday'])],
                  ['Wednesday', Number(jsonDAY[0]['Wednesday'])],
                  ['Thursday', Number(jsonDAY[0]['Thursday'])],
                  ['Friday', Number(jsonDAY[0]['Friday'])],
                  ['Saturday', Number(jsonDAY[0]['Saturday'])]
                );

  /* End Data Collection and Formatting */

  /**
   * Google Charts
   */

  //Load Charts and corechart & barchart packages
  google.charts.load('current', {'packages':['table','corechart', 'controls']});

  //Draw the charts
  google.charts.setOnLoadCallback(drawTable);
  google.charts.setOnLoadCallback(drawPie);
  google.charts.setOnLoadCallback(drawBar);

  var csvTableData; //Gets table data and stores it for export

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
                        top: 40,
                        width:'90%',
                        height:'95%'
                      },
                      backgroundColor: {
                        stroke: '#00178a',
                        strokeWidth: 3,
                      },
                      colors: ['#e11383', '#ffa400', '#45c1e1', '#eb0029', '#95d600', '#978882',
                               '#3366CC','#DC3912','#109618', '#990099','#3B3EAC','#0099C6',
                               '#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11']
                    };


   //Options for Bar Graph
   var columnOptions = {
                          title: 'Average Videos Watched per Day of Week',
                          colors: ['#ffa400'],
                          legend: 'none',
                          bar: { groupWidth: '60%'},
                          chartArea: {
                            'width': '85%',
                            'height': '80%'
                          },
                          backgroundColor: {
                            stroke: '#00178a',
                            strokeWidth: 3,
                          },
                          vAxis: {
                            gridlines: { count: 5 },
                            title: 'Average Videos Watched'
                          },
                          hAxis: {
                            title: 'Day of Week'
                          }
                        };

   //Options for Histogram
   var histoOptions = {
                        title: 'Average Videos Watched',
                        backgroundColor: {
                          stroke: '#00178a',
                          strokeWidth: 3,
                        },
                        colors: [ '#978882', '#1A8763', '#871B47', '#999999'],
                        vAxis: {
                          title: 'Amount of Users',
                        },
                        hAxis: {
                          title: 'Average Videos Watched'
                        }
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

  //Draws the Google Column and Histogram Chart
  function drawBar() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Day of Week');
    data.addColumn('number', 'Amt Vids');
    data.addRows(barChart);

    var bchart = new google.visualization.ColumnChart(document.getElementById('bar_div'));
    bchart.draw(data, columnOptions);

    var histo = new google.visualization.DataTable(); //
    histo.addColumn('string', 'User ID');
    histo.addColumn('string', 'Avg Vids');
    histo.addRows(histoDATA);

    var hchart = new google.visualization.Histogram(document.getElementById('histo_div'));
    hchart.draw(histo, histoOptions);
  }

  /* End Google Charts */

  /**
   * Word Cloud
   */

   //Options for Word Cloud
   var cloudOptions = {
     shape: 'rectangular',
     autoResize: true,
   }

   //add categories to drop down
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
         console.log(key + "=" + value);
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
