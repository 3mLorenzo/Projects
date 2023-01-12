document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  // send email, submit listener to call function

  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view_email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id) {
  console.log(id);

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print result
    console.log(email);
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#view_email').style.display = 'block';

    document.querySelector('#view_email').innerHTML = `
      <div class="border-bottom">
        <h3>From: ${email.sender}</h3>
        <h3>To: ${email.recipients}</h3>
        <p>Subject: ${email.subject}</p>
        <p>${email.timestamp}</p>
      </div>
      <p>${email.body}</p>
      <br>
          `
    if(!email.read) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }


    // archive/unarchive

    const element = document.createElement('button');
    element.className = 'btn btn-secondary';
    if (email.archived) {
      element.innerHTML = 'Unarchive';
    }
    else {
      element.innerHTML = 'Archive';
    }

    element.addEventListener('click', function() {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => { load_mailbox('inbox')})
    });
    document.querySelector('#view_email').append(element);

    // reply

    const reply = document.createElement('button');
    reply.innerHTML = 'Reply';
    reply.className = 'btn btn-secondary';
    reply.addEventListener('click', function() {
      compose_email();
      
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      let subject = email.subject;
      if(subject.split(' ', 1)[0] != "Re:") {
        subject = "Re: " + email.subject;
      }

      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      
    });
    document.querySelector('#view_email').append(reply);

  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view_email').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    emails.forEach(email => {

      const element = document.createElement('div');
      element.innerHTML = `
          <h3>Sender: ${email.sender}</h3>
          <p>${email.subject}</p>
          <br>
          <p>${email.timestamp}
          `;

      if(email.read){
        element.className = "border bg-secondary p-3";
      }
      else {
        element.className = "border bg-light p-3";
      }


      element.addEventListener('click', function() {
        view_email(email.id);
      });

      document.querySelector('#emails-view').append(element);
      })    
    });
};

function send_email(event){

  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const body = document.querySelector('#compose-body').value;
  const subject = document.querySelector('#compose-subject').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
      
  });

}