import ModalFunctionality from 'discourse/mixins/modal-functionality';

export default Ember.Mixin.create(ModalFunctionality, {
  reason: null,
  message: null,
  postEdit: null,
  postAction: null,
  user: null,
  post: null,
  successCallback: null,

  resetModal() {
    this.setProperties({
      reason: null,
      message: null,
      loadingUser: true,
      post: null,
      postEdit: null,
      postAction: 'delete',
      successCallback: null
    });
  },

  finishedSubmission(result) {
    this.send('closeModal');
    let callback = this.get('successCallback');
    if (callback) {
      callback(result);
    }
  }
});
