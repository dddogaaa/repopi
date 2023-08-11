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

            jobsList.innerHTML = 'Total Pages: '+data.total_pages + '<br>' + 'Total Number: '+data.total_num+'<br>'+'<br>';

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
                    File: ${job.File}\n\n`
                );
            
                jobItem.appendChild(radioInput);
                jobItem.appendChild(labelText);
            
                jobItem.classList.add('job-item');

                jobsList.appendChild(jobItem);
            }

            const paginationButtons = document.getElementById('pagination-buttons');
            paginationButtons.innerHTML = '';

            if (data.has_previous) {
                const prevButton = document.createElement('button');
                prevButton.className = 'prev-btn';
                prevButton.textContent = '<<';
                prevButton.className = 'pagination-btn prev-btn';
                prevButton.addEventListener('click', () => loadPage(data.current_page - 1));
                paginationButtons.appendChild(prevButton);
            }

            for (let i = 1; i <= data.total_pages; i++) {
                const pageButton = document.createElement('button');
                pageButton.textContent = i;
                pageButton.className = 'pagination-btn page-btn';
                pageButton.addEventListener('click', () => loadPage(i));
                paginationButtons.appendChild(pageButton);
            }

            if (data.has_next) {
                const nextButton = document.createElement('button');
                nextButton.textContent = '>>';
                nextButton.className = 'pagination-btn next-btn';
                nextButton.addEventListener('click', () => loadPage(data.current_page + 1));
                paginationButtons.appendChild(nextButton);
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
    



