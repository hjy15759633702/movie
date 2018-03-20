INSERT user(name,pwd,email,phone,info,face,uuid,addtime,status) VALUES('hjy1','hjy','767728218@qq.com','15705951952','ª∆º—“’','1.jpg','8603e1899ee9453f886834ca2b320c01','2018-03-16 16:45',0);
INSERT user(name,pwd,email,phone,info,face,uuid,addtime,status) VALUES('hjy2','hjy','757728218@qq.com','15705951951','ª∆º—“’','2.jpg','c724ffc7a34f44b2a71ea90eeb45e113','2018-03-16 16:46',1);
INSERT user(name,pwd,email,phone,info,face,uuid,addtime,status) VALUES('hjy3','hjy','747728218@qq.com','15705951950','ª∆º—“’','3.jpg','3280a89141ee4b0b991d7ce43d245476','2018-03-16 16:47',2);

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