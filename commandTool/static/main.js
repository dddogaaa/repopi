function fetchDjangoViewData(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let jsonString = JSON.stringify(data, null, 2);

            document.getElementById('response_data').innerHTML = jsonString;

            console.log(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}



function loadContent(url) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                document.getElementById('body').innerHTML = xhr.responseText;
                addEventListenersToButtons();
            } else {
                console.error('Error loading content:', xhr.status, xhr.statusText);
                document.getElementById('body').innerHTML = '<p>Error loading content.</p>';
            }
        }
    };

    xhr.open('GET', url, true);
    xhr.send();
        
    if (url === '/jobs/') {
        async function fetchJobs(page) {
            const response = await fetch(`/jobs_data/?page=${page}`);
            const data = await response.json();
            return data;
        }

        async function loadPage(page) {
            const data = await fetchJobs(page);
            const jobsList = document.getElementById('jobs-list');
            jobsList.innerHTML = '';

            jobsList.innerHTML = 'Total Pages: ' + data.total_pages + '<br>' + 'Total Objects: ' + data.total_num + '<br>' + 'Each on Page: ' + data.each_on_page +  '<br>'+'<br>';
           

            for (const job of data.history) {
                const jobItem = document.createElement('label');
            
                const radioInput = document.createElement('input');
                radioInput.type = 'radio';
                radioInput.name = 'jobSelection'; 
                radioInput.value = job.ID; 

                const labelText = document.createTextNode(
                    `ID: ${job.ID}
                    Name: ${job['Command Name']} 
                    Status: ${job.Status} 
                    Command: ${job.Command}
                    Start Time: ${job.Stime}
                    End Time: ${job.Etime}
                    File: ${job.File}\n\n`
                );
            
                jobItem.appendChild(radioInput);
                jobItem.appendChild(labelText);
            
                jobItem.classList.add('job-item');

                jobsList.appendChild(jobItem);
            }

            const paginationButtons = document.getElementById('pagination-buttons');
            paginationButtons.innerHTML = '';

            for (let i = 1; i <= data.total_pages; i++) {
                const pageButton = document.createElement('button');
                pageButton.textContent = i;
                pageButton.className = 'pagination-btn page-btn';
                pageButton.addEventListener('click', () => loadPage(i));
                paginationButtons.appendChild(pageButton);
            }
        }
        loadPage(1);
    }
}

function addEventListenersToButtons() {
    document.getElementById('jobs').addEventListener('click', function() {
        loadContent('/jobs/');
    });

    document.getElementById('repo').addEventListener('click', function() {
        loadContent('/repo/');
    });

    document.getElementById('home').addEventListener('click', function() {
        loadContent('/home/');
    });

    document.getElementById('hello').addEventListener('click', function() {
        fetchDjangoViewData('/repo/hello/');
        console.log('1');
    });

    document.getElementById('getList').addEventListener('click', function() {
        fetchDjangoViewData('/repo/getList/');
        console.log('2');
    });

    document.getElementById('showPath').addEventListener('click', function() {
        fetchDjangoViewData('/repo/showPath/');
        console.log('3');
    });

    document.getElementById('longCmd').addEventListener('click', function() {
        fetchDjangoViewData('/repo/longCmd/');
        console.log('4');
    });

    document.getElementById('wrong').addEventListener('click', function() {
        fetchDjangoViewData('/repo/wrong/');
        console.log('5');
    });

    document.getElementById('mirrorNFF').addEventListener('click', function() {
        fetchDjangoViewData('/repo/mirrorNFF/');
        console.log('6');
    });

    document.getElementById('mirrorU-NFF').addEventListener('click', function() {
        fetchDjangoViewData('/repo/mirrorUpdate/');
        console.log('6');
    });
    document.getElementById('mirrorD-NFF').addEventListener('click', function() {
        fetchDjangoViewData('/repo/mirrorDrop/');
        console.log('6');
    });
}

addEventListenersToButtons();
    
function stream() {
    loadContent('/index/')
    console.log('6');
    const streamButton = document.getElementById('streamButton');

    
    const selectedRadio = document.querySelector('input[name="jobSelection"]:checked');
    
    if (selectedRadio) {
        const selectedValue = selectedRadio.value;
        const url = `/streaming/${selectedValue}/`;

        async function streamData() {
            const response = await fetch(url);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line) {
                        const p = document.createElement('p');
                        p.textContent = line;
                        document.getElementById('output').appendChild(p);
                    }
                }
            }
        }

        streamData();
    } else {
        console.log('No radio button selected.');
    }
}

function fetchData() {
    const command = document.getElementById("cmd").value;
    const status = document.getElementById("status").value;
    const perPage = document.getElementById("each").value;
    const page = document.getElementById("page").value;

    let url = 'http://127.0.0.1:8000/jobs_e/';

    if (command || status || perPage || page) {
        url += '?';

        if (command) {
            url += `command=${command}&`;
        }
        if (status) {
            url += `status=${status}&`;
        }
        if (perPage) {
            url += `each=${perPage}&`;
        }
        if (page) {
            url += `page=${page}&`;
        }

        url = url.slice(0, -1);
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
        const filterElement = document.getElementById("jobs-list");
        filterElement.innerHTML = '';

        filterElement.innerHTML = 'Total Pages: '+ data.total_pages + '<br>' + 'Total Objects: '+ data.total_objects + '<br>' + 'Each on Page: ' + data.each_on_page + '<br>'+'<br>';
    
        const history = data.history;
    
        history.forEach(item => {
            const label = document.createElement("label");
            label.style.display = "block"; 
            label.style.cursor = "pointer";
            
            const radio = document.createElement("input");
            radio.type = "radio";
            radio.name = "jobSelection";
            radio.value = item.ID;
            
            
            label.appendChild(radio);
            
            const labelText = document.createTextNode(
                    `ID: ${item.ID}
                    Name: ${item["Command Name"]} 
                    Status: ${item.Status} 
                    Command: ${item.Command}
                    Start Time: ${item.Stime}
                    End Time: ${item.Etime}
                    File-DIR: ${item["File-DIR"]}\n\n`
                    );
            
            label.appendChild(labelText);
            
            label.addEventListener("click", () => {
                radio.checked = true; 
            });
            
            filterElement.appendChild(label);
        });
    
        
        const paginationButtons = document.getElementById("pagination-buttons");
        paginationButtons.innerHTML = '';
    
        for (let i = 1; i <= data.total_pages; i++) {
            const pageButton = document.createElement("button");
            pageButton.className = "pagination-btn";
            pageButton.textContent = i;
            pageButton.addEventListener("click", () => {
                document.getElementById("page").value = i;
                fetchData(); 
            });
            paginationButtons.appendChild(pageButton);
        }
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
}
    



