$(function(){

  $('#testusername').editable(
    {
      url:'/post',
      type:'text',
      pk:1,
      name:'testusername',
      title:'enter username'
  });

  ///////////////////////////////////////
  //object
  ///////////////////////////////////////
  $('#final-object-name1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_object_name1',
      title:'实物名称',
      
  });

  $('#final-object-members1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_object_members1',
      title:'完成人',
      
  });

  $('#final-object-date1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'date',
      pk:1,
      name:'final_object_date1',
      title:'完成日期',
      
  });

  $('#final-object-comments1').editable(
    {
      mode:'popup',
      url:'/',
      type:'textarea',
      pk:1,
      name:'final_object_comments1',
      title:'备注',
      
  });

  $('#final-object-name2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_object_name2',
      title:'实物名称',
      
  });

  $('#final-object-members2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_object_members2',
      title:'完成人',
      
  });

  $('#final-object-date2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'date',
      pk:1,
      name:'final_object_date2',
      title:'完成日期',
      
  });

  $('#final-object-comments2').editable(
    {
      mode:'popup',
      url:'/',
      type:'textarea',
      pk:1,
      name:'final_object_comments2',
      title:'备注',
      
  });
 ///////////////////////////////////////
  //paper
  ///////////////////////////////////////
  $('#final-paper-name1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_paper_name1',
      title:'论文题目',
      
  });

  $('#final-paper-members1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_paper_members1',
      title:'作者',
      
  });

  $('#final-paper-date1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'date',
      pk:1,
      name:'final_paper_date1',
      title:'完成日期',
      
  });

  $('#final-paper-comments1').editable(
    {
      mode:'popup',
      url:'/',
      type:'textarea',
      pk:1,
      name:'final_paper_comments1',
      title:'期刊/期数',
      
  });
  
    $('#final-paper-name2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_paper_name2',
      title:'论文题目',
      
  });

  $('#final-paper-members2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_paper_members2',
      title:'作者',
      
  });

  $('#final-paper-date2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'date',
      pk:1,
      name:'final_paper_date2',
      title:'完成日期',
      
  });

  $('#final-paper-comments2').editable(
    {
      mode:'popup',
      url:'/',
      type:'textarea',
      pk:1,
      name:'final_paper_comments2',
      title:'期刊/期数',
      
  });
   ///////////////////////////////////////
  //patent
  ///////////////////////////////////////
  $('#final-patent-name1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_patent_name1',
      title:'专利题名',
      
  });

  $('#final-patent-members1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_patent_members1',
      title:'专利申请者',
      
  });

  $('#final-patent-date1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'date',
      pk:1,
      name:'final_patent_date1',
      title:'批准时间',
      
  });

  $('#final-patent-id1').editable(
    {
      mode:'popup',
      url:'/',
      type:'text',
      pk:1,
      name:'final_patent_id1',
      title:'专利号',
      
  });
    $('#final-patent-name2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_patent_name2',
      title:'专利题名',
      
  });

  $('#final-patent-members2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_patent_members2',
      title:'专利申请者',
      
  });

  $('#final-patent-date2').editable(
    {
      mode:'popup',
      url:'/post',
      type:'date',
      pk:1,
      name:'final_patent_date1',
      title:'批准时间',
      
  });

  $('#final-patent-id2').editable(
    {
      mode:'popup',
      url:'/',
      type:'text',
      pk:1,
      name:'final_patent_id2',
      title:'专利号',
      
  });
  
   ///////////////////////////////////////
  //object
  ///////////////////////////////////////
  $('#final-competition-workname1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_competition_workname1',
      title:'竞赛作品名称',
      
  });

  $('#final-competition-members1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'text',
      pk:1,
      name:'final_competition_members1',
      title:'参加人',
      
  });

  $('#final-competition-grade1').editable(
    {
      mode:'popup',
      url:'/post',
      type:'select2',
      value:'1',
      source:[
      	{id:'0',text:'世界级'},
      	{id:'1',text:'国家级'},
      	{id:'2',text:'省级'},
      	{id:'3',text:'市级'},
      	{id:'4',text:'校级'},
      	{id:'5',text:'学院级'},
      ],
      select2:{multiple: false},
      pk:1,
      name:'final_competition_grade1',
      title:'获奖等级',
      
  });

  $('#final-competition-name1').editable(
    {
      mode:'popup',
      url:'/',
      type:'textarea',
      pk:1,
      name:'final_competition_name1',
      title:'获奖名称',
      
  });
 
  
});
