// ADD JQUERY
(function () {
  var tagList = ['Optimus Prime', 'Bumblebee', 'Megatron', 'Ironhide'];
  var $tagList = $("#tagList");
  var $newTag = $("#newTag");

  tagList_render();
  function tagList_render () {
    $tagList.empty();
    tagList.forEach (function (_tag) {
      var temp = '<li>'+ _tag +'<span class="rmTag">&times;</span></li>';
      $tagList.append(temp);
    });
  };

  // Add new tag on "ENTER" press
  $newTag.on('keyup', function (e) {
    if (e.keyCode == 13) {
      var newTag = $("#newTag").val();
      if( newTag.replace(/\s/g, '') !== '' ){
        tagList.push(newTag);
        $newTag.val('');
        tagList_render();
      }
    }
  });

  // Remove Tag
  $tagList.on("click", "li>span.rmTag", function(){
    var index = $(this).parent().index();
    tagList.splice(index, 1);
    tagList_render();
  });
})();
