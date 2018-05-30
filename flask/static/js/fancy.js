window.onload = function() {
  $('#title').html(location.pathname)
  restGet()
}

function restGet(){
  path = location.pathname
  if(path.lastIndexOf('/interfaces/', 0) === 0){
    restGetInterfaces()
  }else if(path == '/interfaces'){
    restGetInterfaces()
  }else{
    restGetGlobal()
  }
}

/*
URL: /
*/

function restGetGlobal(){
  var rest_path = '/api/v1' + location.pathname
  console.log('method: GET')
  console.log('    url:    ' + rest_path)

  $.getJSON(rest_path, function(data){
    console.log('    == response body ==')
    console.log(data)
    console.log('    ===================')

    $("#body").empty();

    if(location.pathname != '/'){
      $('#body').append('<label for="name"><a href="/">/</a></label>')
      $('#body').append('<br/>')
      $('#body').append('<br/>')
    }

    for(key in data.data){
      url = '/' + key
      $('#body').append('<label for="name"><a href="' + url + '">' + key + '</a> : </label>')
      $('#body').append('<input type="text" name="' + key + '" value="' + data.data[key] + '"' +
      ' class="form-control" id="' + key + '">')
      $('#body').append('<button type="button" class="btn btn-default" onclick="restSetGlobal(\'' + key + '\')">設定を更新</button>')
      $('#body').append('<button type="button" class="btn btn-default" onclick="restDeleteGlobal(\'' + key + '\')">設定を削除</button>')
      $('#body').append('<br/>')
      $('#body').append('<br/>')
      console.log('    ' + key + ' : ' + data.data[key])
    }
  })
  .fail(function(){
    $("#body").empty();
    $('#body').append('<label for="name"><a href="/">/</a></label>')
    $('#body').append('<br/>')
    $('#body').append('<br/>')
    $('#body').append('<p>ERROR: 404 Not Found</p>')
    console.log('    Error happens')
  })
}

function restSetGlobal(param){
  var value = $('#' + param).val()
  var url = '/api/v1/' + param
  var json_string = '{"' + param + '":"' + value + '"}'
  console.log('method: PUT')
  console.log('    url:    ' + url)
  console.log('    request body:   ' + json_string)
  $.ajax({url:url, data:json_string, type:'PUT', contentType:'json'});
}

function restDeleteGlobal(param){
  var url = '/api/v1/' + param
  console.log('    method: DELETE')
  console.log('    url:    ' + url)
  $.ajax({url:url, type:'DELETE'});
}

/*
URL: /interfaces/
*/

/*
function restGetInterfaces(){
  var strs = location.pathname.split('/')
  var rest_path = '/api/v1/interfaces/' + strs[strs.length -1]
  console.log('path:      ' + location.pathname)
  console.log('rest path: ' + rest_path)

  $.getJSON(rest_path, function(data){
    $("#body").empty();
    $('#body').append('<label for="name"><a href="/">/</a></label>')
    $('#body').append('<br/>')
    $('#body').append('<br/>')

    if(data.result == false){
      console.log('result false');
      $('#body').append('<label for="name">Not Found</label>')
      $('#body').append('<br/>')
      $('#body').append('<br/>')

    }else{
      console.log(data.data);
    }

    for(index in data.data.interfaces){
      intf = data.data.interfaces[index]
      console.log(intf)
      interfaceName = intf['interface']
      ip = intf['ip']
      id_ip = interfaceName + '_ip'
      subnetmask = intf['subnetmask']
      id_subnemtmask = interfaceName + '_subnetmask'
      up = intf['up']
      id_up = interfaceName + '_up'

      url = '/interfaces/' + interfaceName
      $('#body').append('<label for="name"><a href="' + url + '">' + interfaceName + '</a> : </label>')
      $('#body').append('<input type="text" name="' + id_ip + '" value="' + ip + '"' +
      ' class="form-control" id="' + id_ip + '">')
      $('#body').append('<button type="button" class="btn btn-default" onclick="restSetInterface(\'' + key + '\')">設定を更新</button>')
      $('#body').append('<button type="button" class="btn btn-default" onclick="restDeleteGlobal(\'' + key + '\')">設定を削除</button>')
      $('#body').append('<br/>')
      $('#body').append('<br/>')

      console.log(key)
      console.log(data.data[key])
    }
  });

  console.log('done')
}
*/
