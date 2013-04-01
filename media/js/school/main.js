/**
 * @author tianwei
 * the control js for school page group
 */

// change legend name
// TODO: I will dive into Chartit to add one legend function
$(document).ready(function(){
  if($("tspan").attr("x") === "21")
    {
      alert("test"+$(this).text());
      switch($(this).text())
      {
        case "innovation":
          $(this).text("创新实践");
          break;
        case "enterprise_ee":
          $(this).text("创业训练");
          break;
        case "enterprise":
          $(this).text("创业实践");
          break;
        default:
          break;
      }
    }
});
