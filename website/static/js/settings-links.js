const sidebarLinks = document.querySelectorAll('.sidebar-links a');

const accountContent = document.querySelector('.account-content');
const changeUsernameContent = document.querySelector('.change-username-content');
const changePasswordContent = document.querySelector('.change-password-content');
const deleteAccountContent = document.querySelector('.delete-account-content');

sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {

        sidebarLinks.forEach(link => link.classList.remove('active'));


        accountContent.style.display = 'none';
        changeUsernameContent.style.display = 'none';
        changePasswordContent.style.display = 'none';
        deleteAccountContent.style.display = 'none';

        link.classList.add('active');

        const linkId = link.getAttribute('id');
        if (linkId === 'account-link') {
            accountContent.style.display = 'block';
        } else if (linkId === 'change-username-link') {
            changeUsernameContent.style.display = 'block';
        } else if (linkId === 'change-password-link') {
            changePasswordContent.style.display = 'block';
        } else if (linkId === 'delete-account-link') {
            deleteAccountContent.style.display = 'block';
        }
    });

    if (link.getAttribute('id') === 'account-link') {
        link.classList.add('active');
    }
});
