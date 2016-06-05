/**
 * Created by xuebaoku on 16/5/24.
 */
var curMenu = null, zTree_Menu = null;
var setting = {
	view: {
		showLine: false,
		showIcon: false,
		selectedMulti: false,
		dblClickExpand: false,
		addDiyDom: addDiyDom
	},
	data: {
		simpleData: {
			enable: true
		}
	},
	callback: {
		beforeClick: beforeClick
	}
};


// function addDiyDom(treeId, treeNode) {
// 	var spaceWidth = 5;
// 	var switchObj = $("#" + treeNode.tId + "_switch"),
// 	icoObj = $("#" + treeNode.tId + "_ico");
// 	switchObj.remove();
// 	icoObj.before(switchObj);
//
// 	if (treeNode.level > 1) {
// 		var spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level)+ "px'></span>";
// 		switchObj.before(spaceStr);
// 	}
// }
function addDiyDom(treeId, treeNode) {
    // 取出 li 标签
    var liObj = $("#" + treeNode.tId);
    if (treeNode.open){
        liObj.attr('class','active');
    }
    else{
        liObj.attr('class','treeview');
    }
    // 删除 switchObj 标签
    var switchObj = $("#" + treeNode.tId + "_switch");
    switchObj.remove();
    // 取出 a 标签内容
	var aObj = $("#" + treeNode.tId + "_a");
    aObj.removeAttr();
    aObj.attr('href',treeNode.url);
    aObj.attr('id',treeNode.tId + "_a");
    aObj.attr('target','');
    aObj.empty();
    var editStr = '<i class="fa ' + treeNode.a_class + '"></i>' +
        '<span>' + treeNode.name + '</span>'
        ;
    aObj.append(editStr);
    // 取出 ul 选项
    var UlObj = $("#" + treeNode.tId + "_ul");
	// if ($("#diyBtn_"+treeNode.id).length>0) return;
	// var editStr = "<span id='diyBtn_space_" +treeNode.id+ "' > </span>"
	// 	+ "<button type='button' class='diyBtn1' id='diyBtn_" + treeNode.id
	// 	+ "' title='"+treeNode.name+"' onfocus='this.blur();'></button>";
	// aObj.append(editStr);
	// var btn = $("#diyBtn_"+treeNode.id);
	// if (btn) btn.bind("click", function(){alert("diy Button for " + treeNode.name);});
};


function beforeClick(treeId, treeNode) {
	if (treeNode.level == 0 ) {
		var zTree = $.fn.zTree.getZTreeObj("sidebar-menu_ztree");
		zTree.expandNode(treeNode);
		return false;
	}
	return true;
}

$(document).ready(function(){
	var treeObj = $("#sidebar-menu_ztree");
	$.fn.zTree.init(treeObj, setting, zNodes);
	zTree_Menu = $.fn.zTree.getZTreeObj("sidebar-menu_ztree");
	curMenu = zTree_Menu.getNodes()[0].children[0].children[0];
	zTree_Menu.selectNode(curMenu);

	treeObj.hover(function () {
		if (!treeObj.hasClass("showIcon")) {
			treeObj.addClass("showIcon");
		}
	}, function() {
		treeObj.removeClass("showIcon");
	});
});
