
		var mhand = document.querySelector('.mhand').style;
		var shand = document.querySelector('.shand').style;
		var hhand = document.querySelector('.hhand').style;
		var StartStopButton=document.getElementById("btn");
		var timeswitch;
		
		function clocking() {
			var onoff = StartStopButton.getAttribute("data-on-off");
			
			if (onoff == 0){
				StartStopButton.setAttribute("data-on-off", 1);
				timeswitch = setInterval(startTime, 1000);
			}
			else {
				StartStopButton.setAttribute("data-on-off", 0);
				clearInterval(timeswitch);
			}
		}
		function AxFetch(zid, xid, getnum){
			var ajax = new XMLHttpRequest();
			ajax.onreadystatechange = function() {
			if(this.readyState == 4 && this.status == 200) {
				var ele = document.getElementById(zid);
				var ment = document.getElementById(xid);
				var sigma = this.response;
				var [sig, ma] = sigma.split("|")
				ele.value = ma.slice(0,-1);
				ele.setAttribute("storage", ma.slice(0,-1));
				ment.value = sig;
				ment.setAttribute("storage", sig);
				}
			};
			ajax.open("GET", "front.py?fetch=" + getnum, true)
			ajax.send();
		}
		function AxUpdate(zid, xid, uid)
		{
			var upday = document.getElementById(zid).value;
			var uptime = document.getElementById(xid).value;
			var ajax = new XMLHttpRequest();
			var oldday = document.getElementById(zid).getAttribute("storage");
			var oldtime = document.getElementById(xid).getAttribute("storage");
			ajax.onreadystatechange = function() {
				if(this.readyState == 4 && this.status == 200) {
					var sigma = this.response;
					document.getElementById(uid).innerHTML = sigma;
				}
			};
			ajax.open("GET", "front.py?update=" + upday + "&time=" + uptime + "&oldday=" + oldday + "&oldtime=" + oldtime, true);
			ajax.send();
		}
		function AxRemove(zid, table)
		{
			var ajax = new XMLHttpRequest();
			ajax.onreadystatechange = function() {
				if(this.readyState == 4 && this.status == 200) {
					var ele = document.getElementById('table');
					var sigma = this.response;
					ele.innerHTML = sigma;
				}
			};
			ajax.open("GET", "front.py?delete=" + zid + "&table=" + table, true);
			ajax.send();
		}
		function AxTimes(zid)
		{
		/*		This was an expeariment: Not used
			var d = document.createDocumentFragment();
			d.appendChild(document.getElementsByTagName("LI")[0]);
			d.childNodes[0].childNodes[0].nodeValue = "Heyyo";
			document.getElementsByTagName("UL")[0].appendChild(d);
			*/
			
			var now = new Date().toLocaleTimeString()
			var table = StartStopButton.getAttribute("table")
			
			var ajax = new XMLHttpRequest();
			ajax.onreadystatechange = function() {
				if(this.readyState == 4 && this.status == 200) {
					var element = document.getElementById(zid);
					var htmlReturn = this.response;
					element.innerHTML = htmlReturn;
				}
			};
			ajax.open("GET", "front.py?timein=" + now + "&table=" + table , true);
			if(table == "TableIn") {
				StartStopButton.setAttribute("table","TableOut")
			}
			else {
				StartStopButton.setAttribute("table","TableIn")
			}
			ajax.send();
			
		}
		function startTime() {
			var degToRot = StartStopButton.getAttribute("data-sec")
			shand.transform = 'rotate(' + degToRot + 'deg)';
			shand.transformOrigin = "50% 100%";
			mhand.transform = 'rotate(' + (Number(degToRot) / 60) + 'deg)';
			mhand.transformOrigin = "50% 100%";
			hhand.transform = 'rotate(' + (Number(degToRot) / 360) + 'deg)';
			hhand.transformOrigin = "50% 100%";
			//alert(le.getAttribute("data-sec"));
			StartStopButton.setAttribute("data-sec", Number(degToRot) + 6);
			//document.getElementById("btn").data-sec.value += 6;
		}