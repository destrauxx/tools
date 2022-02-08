class A():
    def valid(self):
        return 'valid'

    def invalid(self):
        return 'invalid'

    def post(self):
        param = True
        if param:
            return self.valid()
        else:
            return self.invalid()

class B(A):

    def post(self):
        print('from b')
        return super().post()


print(B().post())