current_data = []
var gtable;

$(document).ready( function() {
    var table = $('#lapTable').DataTable({
        searchPanes: true
    });
    gtable = table;
});

var socket = io();

socket.on('connect', function() {
    console.log('connection established');
});

socket.on('add_data', function(lap_data) {
    current_data = JSON.parse(lap_data);
    for(idx = 0; idx < current_data.length; idx = idx + 1){
        gtable.row.add([
            current_data[idx].date,
            current_data[idx].lap_num,
            (current_data[idx].lap_time/1000).toString()+' Seconds',
            (current_data[idx].difference/1000).toString()+' Seconds'
        ]).draw();
    }
});

/*
function updateTable(){
    $.getJSON("_times",
        function (data) {
            if(current_data.length < data.length){
                for(idx = current_data.length; idx < data.length; idx = idx + 1){
                    $('#lapTable').dataTable().fnAddData([
                        data[idx].date,
                        data[idx].lap_num,
                        (data[idx].lap_time/1000).toString()+' Seconds',
                        (data[idx].difference/1000).toString()+' Seconds'
                    ])
                }
                current_data = data;
            }
        }
    );
}
*/