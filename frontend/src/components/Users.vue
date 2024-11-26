<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h4>
          Users
          <RouterLink to="/users/create" class="btn btn-primary float-end">
            Add User
          </RouterLink>
        </h4>
      </div>
      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Username</th>
              <th>Roles</th>
              <th>Timezone</th>
              <th>Active</th>
              <th>Created</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody v-if="users.length > 0">
            <tr v-for="(user, index) in users" :key="index">
              <td class="align-middle">{{ user.username }}</td>
              <td>
                <ul v-for="role in user.roles" :key="role" class="list-group">
                  <li class="list-group-item border-0">{{ role }}</li>
                </ul>
              </td>
              <td class="align-middle">{{ user.preferences.timezone }}</td>
              <td class="align-middle">{{ user.active }}</td>
              <td class="align-middle">
                {{ new Date(user.created_ts).toISOString() }}
              </td>
              <td class="align-middle text-center">
                <RouterLink
                  :to="{ path: '/users/' + user._id + '/edit' }"
                  class="btn btn-success me-1"
                >
                  Edit
                </RouterLink>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="openConfirmationModal(user._id, user.username)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="6" class="text-center">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <Modal
      v-if="showModal"
      title="Confirm Delete"
      :body="`Are you sure you want to delete this user? ${userToDelete}`"
      confirmText="Delete"
      :isVisible="showModal"
      @close="handleClose"
      @confirm="deleteUser"
    />
  </div>
</template>

<script>
import Modal from '../components/Modal.vue'

export default {
  name: 'Users',
  components: {
    Modal,
  },
  data() {
    return {
      users: [],
      showModal: false,
      userIdToDelete: null,
      userToDelete: null,
    }
  },
  mounted() {
    this.getUsers() // Fetch users when the component is mounted
  },
  methods: {
    // Fetch users from the API
    async getUsers() {
      try {
        const url = import.meta.env.VITE_API_URL + '/users'
        const response = await fetch(url)
        
        // Check if the response is successful
        if (!response.ok) {
          throw new Error(`Failed to fetch: ${response.statusText}`)
        }

        const data = await response.json()
        
        // Ensure the expected structure of the response
        if (data && data.data) {
          this.users = data.data
        } else {
          console.error('Unexpected response structure:', data)
        }
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    },

    // Open confirmation modal to delete a user
    openConfirmationModal(userId, username) {
      this.userIdToDelete = userId
      this.userToDelete = username
      this.showModal = true
    },

    // Delete a user
    async deleteUser() {
      if (!this.userIdToDelete) return

      try {
        const url = `${import.meta.env.VITE_API_URL}/delete_user/${this.userIdToDelete}`
        const response = await fetch(url, {
          method: 'DELETE',
        })
        
        // Check if the response is successful
        if (!response.ok) {
          throw new Error(`Failed to delete user: ${response.statusText}`)
        }
        
        // Remove the deleted user from the list
        this.users = this.users.filter(user => user._id !== this.userIdToDelete)

        // Close the modal and reset the selected user data
        this.showModal = false
        this.userIdToDelete = null
        this.userToDelete = null
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    },

    // Close the modal without deleting
    handleClose() {
      this.showModal = false
      this.userIdToDelete = null
      this.userToDelete = null
    },
  },
}

</script>
