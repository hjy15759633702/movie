INSERT user(name,pwd,email,phone,info,face,uuid,addtime,status) VALUES('hjy1','hjy','767728218@qq.com','15705951952','黄佳艺','1.jpg','8603e1899ee9453f886834ca2b320c01','2018-03-16 16:45',0);
INSERT user(name,pwd,email,phone,info,face,uuid,addtime,status) VALUES('hjy2','hjy','757728218@qq.com','15705951951','黄佳艺','2.jpg','c724ffc7a34f44b2a71ea90eeb45e113','2018-03-16 16:46',1);
INSERT user(name,pwd,email,phone,info,face,uuid,addtime,status) VALUES('hjy3','hjy','747728218@qq.com','15705951950','黄佳艺','3.jpg','3280a89141ee4b0b991d7ce43d245476','2018-03-16 16:47',2);

INSERT comment(content,addtime,movie_id,user_id) VALUES('good','2018-03-16 16:47',1,1);
INSERT comment(content,addtime,movie_id,user_id) VALUES('goodad','2018-03-16 16:47',1,2);
INSERT comment(content,addtime,movie_id,user_id) VALUES('goodad','2018-03-16 16:47',2,1);
INSERT comment(content,addtime,movie_id,user_id) VALUES('gooddad','2018-03-16 16:47',2,1);
INSERT comment(content,addtime,movie_id,user_id) VALUES('gadadoodad','2018-03-16 16:47',2,2);
INSERT comment(content,addtime,movie_id,user_id) VALUES('goodadadad','2018-03-16 16:47',1,1);
INSERT comment(content,addtime,movie_id,user_id) VALUES('gadadoodadadad','2018-03-16 16:47',2,2);


INSERT moviecol(addtime,movie_id,user_id) VALUES('2018-03-16 16:47',2,2);
INSERT moviecol(addtime,movie_id,user_id) VALUES('2018-03-16 16:47',1,1);
INSERT moviecol(addtime,movie_id,user_id) VALUES('2018-03-16 16:47',2,1);
INSERT moviecol(addtime,movie_id,user_id) VALUES('2018-03-16 16:47',1,2);
INSERT moviecol(addtime,movie_id,user_id) VALUES('2018-03-16 16:47',2,2);

INSERT userlog(ip,addtime,user_id) VALUES('127.0.0.1','2018-03-16 16:47',1);
INSERT userlog(ip,addtime,user_id) VALUES('127.0.0.2','2018-03-16 15:47',2);
INSERT userlog(ip,addtime,user_id) VALUES('127.0.0.3','2018-03-16 14:47',2);
INSERT userlog(ip,addtime,user_id) VALUES('127.0.0.4','2018-03-16 13:47',1);
INSERT userlog(ip,addtime,user_id) VALUES('127.0.0.4','2018-03-16 13:47',1);
INSERT userlog(ip,addtime,user_id) VALUES('127.0.0.4','2018-03-16 13:47',1);

# 权限
INSERT auth(id,name,url,addtime) VALUES(1,'/admin/','/admin/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(2,'/admin/tag/add/','/admin/tag/add/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(3,'/admin/tag/list/<int:page>/','/admin/tag/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(4,'/admin/tag/del/<int:id>/','/admind/tag/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(5,'/admin/tag/edit/<int:id>/','/admin/tag/edit/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(6,'/admin/movie/add/','/admin/movie/add/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(7,'/admin/movie/list/<int:page>/','/admin/movie/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(8,'/admin/movie/del/<int:id>/','/admin/movie/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(9,'/admin/movie/edit/<int:id>/','/admin/movie/edit/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(10,'/admin/preview/add/','/admin/preview/add/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(11,'/admin/preview/list/<int:page>/','/admin/preview/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(12,'/admin/preview/del/<int:id>/','/admin/preview/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(13,'/admin/preview/edit/<int:id>/','/admin/preview/edit/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(14,'/admin/user/list/<int:page>/','/admin/user/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(15,'/admin/user/view/<int:id>/','/admin/user/view/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(16,'/admin/user/del/<int:id>/','/admin/user/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(17,'/admin/user/freeze/<int:id>/','/admin/user/freeze/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(18,'/admin/user/unfreeze/<int:id>/','/admin/user/unfreeze/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(19,'/admin/comment/list/<int:page>/','/admin/comment/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(20,'/admin/comment/del/<int:id>/','/admin/comment/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(21,'/admin/moviecol/list/<int:page>/','/admin/moviecol/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(22,'/admin/moviecol/del/<int:id>/','/admin/moviecol/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(23,'/admin/adminloginlog/list/<int:page>/','/admin/adminloginlog/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(24,'/admin/userloginlog/list/<int:page>/','/admin/userloginlog/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(25,'/admin/oplog/list/<int:page>/','/admin/oplog/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(26,'/admin/role/add/','/admin/role/add/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(27,'/admin/role/list/<int:page>/','/admin/role/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(28,'/admin/role/del/<int:id>/','/admin/role/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(29,'/admin/role/edit/<int:id>/','/admin/role/edit/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(30,'/admin/auth/add/','/admin/auth/add/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(31,'/admin/auth/list/<int:page>/','/admin/auth/list/<int:page>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(32,'/admin/auth/del/<int:id>/','/admin/auth/del/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(33,'/admin/auth/edit/<int:id>/','/admin/auth/edit/<int:id>/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(34,'/admin/admin/add/','/admin/admin/add/','2018-03-21 15:59:00');
INSERT auth(id,name,url,addtime) VALUES(35,'/admin/admin/list/<int:page>/','/admin/admin/list/<int:page>/','2018-03-21 15:59:00');

INSERT role(id,name,auths,addtime) VALUES(1,'superAdmin','1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35','2018-03-21 15:59:00');


