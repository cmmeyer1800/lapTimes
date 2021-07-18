current_data = []

$(document).ready( function() {
    var table = $('#lapTable').DataTable({
        searchPanes: true
    });
    //table.searchPanes.container().prependTo(table.table().container());
    //table.searchPanes.resizePanes();
});

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
setInterval('updateTable()', 3000);