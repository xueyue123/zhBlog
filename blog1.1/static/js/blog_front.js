
function category_article_list(id) { //显示分类文章列表
        window.location.href = "/category/?id=" + id.id; //如果点击了分类列表中的分类，则跳转到该分类下所有文章页面
}

function read_article(id) { //显示文章内容
        window.location.href = "/article/?id=" + id.id;
}

function read_essays(id) { //显示随笔内容
        window.location.href = "/essays/?id=" + id.id;
}

function commit_comment(id) { //提交评论
        var nickname = $("#comment_nickname").val();
        var content = $("#comment_content").val();
        if (nickname == "") {
                alert("昵称不能为空!");
                return;
        } else if (content == "") {
                alert("评论内容不能为空")
                return;
        }
        $.get("/commit_comment/", {
                "id": id.id,
                "nickname": nickname,
                "content": content
        }, function(ret) {
                if (ret == "1") {
                        alert("昵称不能为空");
                } else if (ret == "2") {
                        alert("评论内容不能为空");
                } else {
                        alert(ret);
                }
        });
}

function commit_message() { //提交留言
        var nickname = $("#nickname").val();
        var title = $("#message_title").val();
        var content = $("#message_content").val();
        if (nickname == "") {
                alert("昵称不能为空!");
                return;
        } else if (title == "") {
                alert("标题不能为空")
                return;
        } else if (content == "") {
                alert("内容不能为空");
                return;
        }
        $.get("/commit_message/", {
                "nickname": nickname,
                "title": title,
                "content": content
        }, function(ret) {
                alert(ret);
                location.reload(true);
        });
}
